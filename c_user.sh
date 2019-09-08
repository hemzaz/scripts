#!/bin/bash

die()
{
	local _ret=$2
	test -n "$_ret" || _ret=1
	test "$_PRINT_HELP" = yes && print_help >&2
	echo "$1" >&2
	exit ${_ret}
}

begins_with_short_option()
{
	local first_option all_short_options='h'
	first_option="${1:0:1}"
	test "$all_short_options" = "${all_short_options/$first_option/}" && return 1 || return 0
}
_positionals=()

print_help()
{
	printf '%s\n' "The general script's help msg"
	printf 'Usage: %s [-h|--help] <first> <second> [<third>]\n' "$0"
	printf '\t%s\n' "<first>: The first argument"
	printf '\t%s\n' "<second>: The second argument"
	printf '\t%s\n' "<third>: The third argument"
	printf '\t%s\n' "<fourth>: The fourth argument"
	printf '\t%s\n' "-h, --help: Prints help"
}

parse_commandline()
{
	_positionals_count=0
	while test $# -gt 0
	do
		_key="$1"
		case "$_key" in
			-h|--help)
				print_help
				exit 0
				;;
			-h*)
				print_help
				exit 0
				;;
			*)
				_last_positional="$1"
				_positionals+=("$_last_positional")
				_positionals_count=$((_positionals_count + 1))
				;;
		esac
		shift
	done
}

handle_passed_args_count()
{
	local _required_args_string="'first'"
	test "${_positionals_count}" -le 1 || _PRINT_HELP=yes die "FATAL ERROR: There were no positional arguments}')." 1
}

assign_positional_args()
{
	local _positional_name _shift_for=$1
	_positional_names="_arg_first _arg_second _arg_third _arg_fourth "

	shift "$_shift_for"
	for _positional_name in ${_positional_names}
	do
		test $# -gt 0 || break
		eval "$_positional_name=\${1}" || die "Error during argument parsing" 1
		shift
	done
}

parse_commandline "$@"
handle_passed_args_count
assign_positional_args 1 "${_positionals[@]}"

echo "Value of first argument: $_arg_first"
echo "Value of second argument: $_arg_second"
echo "Value of third argument: $_arg_third"
echo "Value of fourth argument: $_arg_fourth"

for i in "${_positionals[@]}"
 do
 	[[-f $i]]
 	then
 		USERN=$(cut -d " " -f 1 $i)
 		NAME=$(cut -d " " -f 2 $i)
 		USERG=$(cut -d " " -f 3 $i)
 		SCRPT=$(cut -d " " -f 4 $i)
 		useradd -g $USERG -m $USER && $SCRPT && \
 		echo "$USER Created successfully"
 	else
 		die "FATAL ERROR: --- $i is not a valid path"
 	fi
 done

 exit 0