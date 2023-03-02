import os
import sys

# import shutil
import subprocess
import pathlib
from typing import Sequence


def query_yes_no(question: str, default: str = "yes") -> bool:
    """
    Ask a yes/no question via input() and return their answer.

    Args:
        question (str): The question presented to the user
        default (str, optional): is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user). Defaults to "yes".

    Raises:
        ValueError: in case of an invalid default.

    Returns:
        bool: True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower().strip()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")


def query_options(question: str, options: Sequence[str], default: int = 0) -> str:
    """
    Ask the user to choose one of the options via input() and return their answer.

    Args:
        question (str):  Question that is presented to the user.
        options (Sequence[str]): List of options among which the user can choose.
        default (int, optional): is the presumed answer if the user just hits <Enter>.
            It must be an integer in the range [0, len(options)].
            Defaults to 0.

    Raises:
        ValueError: in case of an invalid default answer.

    Returns:
        str: The chosen option from options.
    """
    if not isinstance(options, Sequence) or len(options) == 0:
        raise ValueError("Options must be a Sequence of length > 0.")
    if not (0 <= default < len(options)):
        raise ValueError(f"Default value must be in range (0, {len(options)}).")

    prompt = f"[{default}]\n" + "\n".join(
        [f"[{i}] - {option}" for i, option in enumerate(options)]
    )

    valid = [str(i) for i in range(0, len(options))]

    while True:
        sys.stdout.write(question + prompt + "\n")
        choice = input().lower().strip()
        if choice == "":
            return options[default]
        elif choice in valid:
            return options[int(choice)]
        else:
            sys.stdout.write(
                "Please respond with a number " f"from 0 to {len(options)-1}.\n"
            )


def query_field(question: str, default: str = None, len_limit: int = 100) -> str:
    """
    Ask a question via input() and return their answer.

    Args:
        question (str): The question presented to the user
        default (str, optional): is the presumed answer if the user just hits <Enter>.
            It must be a string or None (meaning an answer is required of the user).
            Defaults to None.
        len_limit (int, optional): maximal number of characters that an answer
            can have and still be accepted. Defaults to 100.

    Raises:
        ValueError: In case of an invalid default

    Returns:
        str: The answer the user has given (or default)
    """
    if default is None:
        prompt = "  "
    elif isinstance(default, str):
        prompt = f" [{default}] "
    else:
        raise ValueError(f"invalid default answer: '{default}'")

    while True:
        sys.stdout.write(question + prompt)
        user_answer = input().strip()
        if default is not None and user_answer == "":
            return default
        elif 0 < len(user_answer) < len_limit:
            return user_answer
        else:
            sys.stdout.write(
                f"Please respond with a non-empty answer that "
                f"has less than {len_limit} characters.\n"
            )


if __name__ == "__main__":

    # Control flow:
    # 1. Creating link to data
    link_to_data = query_yes_no(
        "Would you like to link to a data directory on your machine?", default="no"
    )
    if link_to_data:
        while True:
            data_path = query_field(
                "At which path is your data directory located?", default=None
            )

            if os.path.exists(data_path) and os.path.isdir(data_path):
                # Transform into pathlib object for handy operations
                data_path = pathlib.PurePath(data_path)

                # Create symlink
                print("Ok, creating the link.")
                os.symlink(
                    src=data_path,
                    dst=os.path.join(
                        os.path.abspath(os.curdir),
                        os.path.basename(data_path),
                    ),
                )

                # Add data path to .gitignore
                with open(".gitignore", "a") as f:
                    f.write(
                        "\n\n"
                        + "# Ignore data folder\n"
                        + data_path.name
                        + "\n"
                        + data_path.name
                        + "/"
                        + "\n"
                        "." + data_path.name + "/"
                    )

                break

            else:
                print(
                    f"The path {data_path} does not exist or is not a directory. "
                    "Please enter a valid path."
                )

    # 2. Creating link to github repo
    create_repo = query_yes_no(
        "Would you like to link this repository to a repository on github.com?",
        default="no",
    )
    if create_repo:
        # Query repo name and owner from user
        repo_name = query_field(
            "What is name of the github.com repository you wish to link to?",
            default="{{cookiecutter.repository_name}}",
            len_limit=100,
        )

        repo_owner = query_field(
            "What is the name of the owner (user/organisation) of the repository?",
            default="James Bond",
            len_limit=30,
        )

        # Set user name and email for first commit
        user_name = "james-bond"
        user_email = "jamesbond@cookiecutter.org"

        # Derived variables
        repo_url = "git@github.com:" + repo_owner + "/" + repo_name + ".git"
        print(f"Linking to {repo_url}.")

        try:
            # Initialize project as git repository
            subprocess.call(["git", "init"])

            # Configure git username and email
            subprocess.call(["git", "config", "user.name", user_name])
            subprocess.call(["git", "config", "user.email", user_email])

            # Add remote at the repository URL
            subprocess.call(["git", "remote", "add", "origin", repo_url])
            subprocess.call(["git", "add", "-A"])
            subprocess.call(["git", "commit", "-m", "Initalization 🚀"])
            subprocess.call(["git", "push", "-u", "origin", "master"])

            # Unset the user name and email form "cookiecutter" so user can use his own.
            subprocess.call(["git", "config", "--unset", "user.name"])
            subprocess.call(["git", "config", "--unset", "user.email"])

        except Exception as e:
            print("Github link creation failed. Please link the repo manually.")
            print(e)

    # 3. Creating conda environment
    # TODO: Add venv environment creation as alternative
    create_conda_env = query_yes_no(
        "Would you like to create a project environment using conda?", default="no"
    )
    if create_conda_env:
        # Check that conda command exists
        from distutils.spawn import find_executable

        if find_executable("conda") is None:
            print(
                "\U0001F635 No conda executable found. Please first install conda on "
                "your machine and add it to the PATH. "
                "Then call `make create_environment`."
            )
        else:
            try:
                # Call conda executable to create environment
                subprocess.call("make create_environment".split(" "))

                # Update conda config to show only the short name of the env.
                subprocess.call("conda config --set env_prompt '({name})'".split(" "))

                # TODO: Automatic Jupyter notebook installation fails due to
                # not working conda activate ./env
                # if query_yes_no(
                #    "Would you like to install jupyter tools?", default="no"
                # ):
                #    subprocess.call("conda init".split(" "))
                #    subprocess.call("conda activate ./env".split(" "))
                #    subprocess.call("make install_jupyter_tools".split(" "))

            except Exception as e:
                print("Environment creation failed. Please create environment manually")
                print(e)

    os.chdir("..")
