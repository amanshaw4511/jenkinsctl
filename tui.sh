#!/usr/bin/env bash

trap "echo 'Exiting on Ctrl+C'; exit 1" SIGINT

# Function to check if the selected string is a folder name (enclosed in [ ])
_is_folder_name() {
	echo "$@" | grep -o '\[[^][]*\]' > /dev/null
}

# Function to extract the folder name from a string enclosed in [ ]
_extract_folder_name() {
	echo "$@" | sed 's/\[\(.*\)\]/\1/'
}

# Function to list jobs using jenkinsctl and fzf
_list_jobs() {
	local FOLDER_NAME="$@"
	echo $( jenkinsctl jobs "$FOLDER_NAME" | fzf )
}


# Function to list build and return selected build no. by fzf
_list_builds() {
	local JOB_NAME="$@"
	echo $( jenkinsctl list "$JOB_NAME" \
		| awk 'NR>1 { print $1 }' \
		| fzf --header "Select build no."\
	)
}


_list_build_actions() {
	echo $( echo -e "rebuild\nconfig\njson\nlogs" \
		| fzf --header "Select action to perform"
	)
}

_handle_job_view() {
	local JOB_NAME="$1"

	[ -z "$JOB_NAME" ] && echo ":::: Quiting... selected job name is empty" && exit 1
	local build_no=$( _list_builds "$JOB_NAME" )

	[ -z "$build_no" ] && echo ":::: Quiting... selected build no. is empty" && exit 1
	local action=$(_list_build_actions)

	[ -z "$action" ] && echo ":::: Quiting selected action is empty" && exit 1

	echo ":::: Selected action: '$action' for job name: '$JOB_NAME' and build no: '$build_no"

	jenkinsctl "$action" "$JOB_NAME" "$build_no"
}

	
# Recursive function to navigate folders or do actions
run() {
	local CURRENT_FOLDER="$1"
	
	echo ":::: Listing job in folder: $CURRENT_FOLDER"

	local selected_job=$(_list_jobs "$1")
	echo ":::: Selected: $selected_job"

	# exit if ctrl+c is pressed in fzf, selected_job value will be empty
	[ -z "$selected_job" ] && echo ":::: Quiting... selected folder/job is empty" && exit 1


	if _is_folder_name "$selected_job"
	then
		local folder_name=$( _extract_folder_name "$selected_job" )

		echo ":::: Entering folder: $folder_name"
		run "$CURRENT_FOLDER/$folder_name"
		exit 0
	fi

	_handle_job_view "$CURRENT_FOLDER/$selected_job"
}

run "$1"
