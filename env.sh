# SPDX-License-Identifier: BSD-3-Clause

# Check to see if we were sourced and not ran directly
(
  [[ -n $ZSH_VERSION && $ZSH_EVAL_CONTEXT =~ :file$ ]] ||
  [[ -n $BASH_VERSION ]] && (return 0 2>/dev/null)
) && _IS_SOURCED=1 || _IS_SOURCED=0

if [ $_IS_SOURCED -eq 0 ]; then
	echo "ERROR: You must source this script, not run it."
	exit 1
fi

_GET_SCRIPT_DIR() {
	if [ -n "${BASH_VERSION:-}" ]; then
		_SH_PATH=$(readlink -f "${BASH_SOURCE:-$0}")
		echo $(dirname "$_SH_PATH")
	fi
	if [ -n $ZSH_VERSION ];then
		echo "${0:a:h}"
	fi
}



# Exit the Xylene environment
deactivate() {
	# Reset path
	if [ -n "${_OLD_ENV_PATH:-}" ]; then
		PATH="${_OLD_ENV_PATH:-}"
		export PATH
		unset _OLD_ENV_PATH
	fi

	if [ -n "${_OLD_VIRTUAL_PYTHONHOME:-}" ] ; then
		PYTHONHOME="${_OLD_VIRTUAL_PYTHONHOME:-}"
		export PYTHONHOME
		unset _OLD_VIRTUAL_PYTHONHOME
	fi

	if [ -n "${PYTHONPATH:-}" ]; then
		PYTHONPATH="${_OLD_PYTHON_PATH:-}"
		export PYTHONPATH
		unset _OLD_PYTHON_PATH
	fi

	if [ -n "${BASH_VERSION:-}" -o -n "${ZSH_VERSION:-}" ]; then
		hash -r 2> /dev/null
	fi

	if [ -n "${_OLD_ENV_PS1:-}" ]; then
		PS1="${_OLD_ENV_PS1:-}"
		export PS1
		unset _OLD_ENV_PS1
	fi

	unset _IS_SOURCED
	unset XYLENE_ENV
	unset _PY_EXEC
	unset _PY_VERS
	unset _PY_HAS_VENV
	unset _PY_VENV_DIR
	unset XYLENE_VIVADO_DIR
	unset _VIVADO_VERSION
	unset XILINX_VIVADO
	unset XYLENE_WORKING_DIR

	if [ ! "${1:-}" = "dontimplode" ]; then
		echo "[*] bye bye!"
		unset -f deactivate
		unset -f _GET_SCRIPT_DIR
	fi

}

deactivate dontimplode

# Setup Initial env
XYLENE_ENV="$(_GET_SCRIPT_DIR)"
export XYLENE_ENV
XYLENE_WORKING_DIR="${XYLENE_ENV}/.xylene"
export XYLENE_WORKING_DIR
XYLENE_TOOL_FILE="${XYLENE_ENV}/.xylene-settings.sh"


# If there is no directory, make it
if [ ! -d "$XYLENE_WORKING_DIR" ]; then
	mkdir "${XYLENE_WORKING_DIR}"
cat << EOT > "${XYLENE_WORKING_DIR}/.gitignore"
*
!.gitignore
EOT
fi

# If there is not user settings file, dump a new one
if [ ! -f "$XYLENE_TOOL_FILE" ]; then
cat << EOT > "${XYLENE_TOOL_FILE}"
# SPDX-License-Identifier: BSD-3-Clause

# Check to see if we were sourced and not ran directly
(
  [[ -n \$ZSH_VERSION && \$ZSH_EVAL_CONTEXT =~ :file$ ]] ||
  [[ -n \$BASH_VERSION ]] && (return 0 2>/dev/null)
) && _IS_SOURCED=1 || _IS_SOURCED=0

if [ \$_IS_SOURCED -eq 0 ]; then
	echo "ERROR: You must source this script, not run it."
	exit 1
fi

# !! EDIT BELOW THIS LINE !! #

# Use this area to setup any paths you need
# Also make sure that Xylene can see Vivado

_VIVADO_VERSION="\${XYLENE_VIVADO_VERSION:-2022.1}"
if [ -z \$XYLENE_VIVADO_DIR ]; then
	export XYLENE_VIVADO_DIR="/tools/Xilinx/Vivado/\${_VIVADO_VERSION}"
fi
EOT
fi

# Load user settings
source "${XYLENE_TOOL_FILE}"

# Check to make sure we can init the Vivado env
if [ ! -d "$XYLENE_VIVADO_DIR" ]; then
	echo "ERROR: The specified Vivado directory ($XYLENE_VIVADO_DIR) does not exist"
	return 1
fi

export XILINX_VIVADO="${XYLENE_VIVADO_DIR}"

# Check to see if we have python
_PY_EXEC=$(command -v python)
_PY_VERS=
if [ -z "$_PY_EXEC" ]; then
	echo "ERROR: Unable to find python exeutable"
	return 1
else
	_PY_VERS=$($_PY_EXEC --version)
fi

_PY_HAS_VENV=$($_PY_EXEC -c "import importlib;v=importlib.util.find_spec('venv');print('0' if v is not None else '1')")

if [ $_PY_HAS_VENV -eq 1 ]; then
	echo "ERROR: Python needs to have the 'venv' module."
	return 1
fi

echo "[*] Initializing python venv"
_PY_VENV_DIR="${XYLENE_WORKING_DIR}/python-venv"
if [ ! -d "$_PY_VENV_DIR" ]; then
	$_PY_EXEC -m venv $_PY_VENV_DIR
fi

if [ -n "${PYTHONHOME:-}" ]; then
	_OLD_VIRTUAL_PYTHONHOME="${PYTHONHOME:-}"
	unset PYTHONHOME
fi

if [ -z "${PYTHONPATH:-}" ]; then
	_OLD_PYTHON_PATH="${PYTHONPATH:-}"
	export PYTHONPATH="${XYLENE_ENV}/pylibs:${XYLENE_NATIVE_BUILD_DIR}/bindings/python:${_OLD_PYTHON_PATH}"
fi

_OLD_ENV_PATH="$PATH"
PATH="${XYLENE_ENV}/utilities:${XYLENE_WORKING_INSTALL_DIR}/bin:${_PY_VENV_DIR}/bin:${XILINX_VIVADO}/bin:$PATH"
export PATH

if [ -n "${BASH_VERSION:-}" -o -n "${ZSH_VERSION:-}" ]; then
	hash -r 2> /dev/null
fi

if [ ! -f "${_PY_VENV_DIR}/.xylene-init" ]; then
	echo "[*] Setting up python venv"
	python -m pip install --upgrade pip
	pip install -r $XYLENE_ENV/requirements.txt
	touch "${_PY_VENV_DIR}/.xylene-init"
fi

# Pull the DBs
git submodule update --init --recursive

_OLD_ENV_PS1="${PS1:-}"
PS1="(PRJXYLENE) ${PS1:-}"
export PS1

echo "[*] To leave the prjxylene environment, run the command 'deactivate'"
echo "[*] Happy Hacking"
