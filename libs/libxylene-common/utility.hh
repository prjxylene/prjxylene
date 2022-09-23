/* SPDX-License-Identifier: BSD-3-Clause */
/* libxylene-common/utility.hh - Useful miscellaneous bits */
#pragma once
#if !defined(xylene_common_utility_hh)
#define xylene_common_utility_hh

#include <cstdint>
#include <type_traits>

namespace Xylene::Common::Utility {
	namespace Units {
		/* IEC Units*/
		constexpr std::uint64_t operator ""_KiB(const unsigned long long value) noexcept { return std::uint64_t(value) * 1024; }
		constexpr std::uint64_t operator ""_MiB(const unsigned long long value) noexcept { return std::uint64_t(value) * 1048576; }
		constexpr std::uint64_t operator ""_GiB(const unsigned long long value) noexcept { return std::uint64_t(value) * 1073741824; }
		constexpr std::uint64_t operator ""_TiB(const unsigned long long value) noexcept { return std::uint64_t(value) * 1099511627776; }
		constexpr std::uint64_t operator ""_PiB(const unsigned long long value) noexcept { return std::uint64_t(value) * 1125899906842624; }

		/* SI Units */
		constexpr std::uint64_t operator ""_KB(const unsigned long long value) noexcept { return std::uint64_t(value) * 1000; }
		constexpr std::uint64_t operator ""_MB(const unsigned long long value) noexcept { return std::uint64_t(value) * 1000000; }
		constexpr std::uint64_t operator ""_GB(const unsigned long long value) noexcept { return std::uint64_t(value) * 1000000000; }
		constexpr std::uint64_t operator ""_TB(const unsigned long long value) noexcept { return std::uint64_t(value) * 1000000000000; }
		constexpr std::uint64_t operator ""_PB(const unsigned long long value) noexcept { return std::uint64_t(value) * 1000000000000000; }
	}

	namespace Types {
		using ssize_t = typename std::make_signed<std::size_t>::type;
		using off_t   = std::int64_t;
	}
}

#endif /*xylene_common_utility_hh*/
