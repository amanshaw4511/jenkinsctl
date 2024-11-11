#!/usr/bin/env bash

trap "echo 'Exiting on Ctrl+C'; exit 1" SIGINT
set -e # # Exit immediately if a command exits with a non-zero status


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


# Function to list build and return selected build number by fzf
_list_builds() {
	local JOB_NAME="$@"
	local builds=$(jenkinsctl list "$JOB_NAME" \
		| awk 'NR>1'
	)
	local options="<Refresh>\n${builds}\n<Back>"

	current_job="$JOB_NAME"
	echo -e "$options" \
		| fzf --header "Select build no." \
		| awk '{ print $1 }'
}


# Function to list build actions
_list_build_actions() {
	local actions=$(cat <<- EOF
		rebuild
		config
		json
		logs
		edit and rebuild
		<Back>
	EOF
	)

	echo $( echo "$actions" \
		| fzf --header "Select action to perform"
	)
}


# Function to edit and rebuild
_edit_and_rebuild_action() {
	local JOB_NAME="$1"
	local BUILD_NUMBER="$2"
	local config_file=$(mktemp)

	jenkinsctl config "$JOB_NAME" "$BUILD_NUMBER" > "$config_file"
	nvim "$config_file"
	jenkinsctl build -f "$config_file"
}


# Function to list/show jobs view
_handle_job_view() {
	local JOB_NAME="$1"
	[ -z "$JOB_NAME" ] && echo ":::: Quiting... selected job name is empty" && exit 1

	local build_no=$( _list_builds "$JOB_NAME" )
	[ -z "$build_no" ] && echo ":::: Quiting... selected build no. is empty" && exit 1


	if [ "$build_no" = "<Refresh>" ]; then
		_handle_job_view "$JOB_NAME"
		return 0
	fi
	if [ "$build_no" = "<Back>" ]; then
		return 0
	fi

	local action=$(_list_build_actions)
	[ -z "$action" ] && echo ":::: Quiting selected action is empty" && exit 1


	if [ "$action" = "<Back>" ]; then
		_handle_job_view "$JOB_NAME"
		return 0
	fi

	echo ":::: Selected action: '$action' for job name: '$JOB_NAME' and build no: '$build_no"

	if [ "$action" = "edit and rebuild" ]; then
		_edit_and_rebuild_action "$JOB_NAME" "$build_no"
	else
		jenkinsctl "$action" "$JOB_NAME" "$build_no"
	fi

	read -p "Press Enter key to CONTINUE, Ctrl + C to QUIT"

	if [ "$?" = "0" ]
	then 
		_handle_job_view "$JOB_NAME"
	fi
	return 0
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

	if [ "$?" = 0 ]
	then
		run "$CURRENT_FOLDER"
	fi

}

run "$1"
