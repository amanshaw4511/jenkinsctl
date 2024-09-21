def handle_enable_completion(shell: str):
    if shell == "bash":
        print("\n# To enable autocompletion for bash, add the following to your ~/.bashrc:")
        print("echo 'eval \"$(_JENKINSCTL_COMPLETE=bash_source jenkinsctl)\"' >> ~/.bashrc")
        print("\n# Then reload your bash configuration:")
        print("source ~/.bashrc")

    elif shell == "zsh":
        print("\n# To enable autocompletion for zsh, add the following to your ~/.zshrc:")
        print("echo 'eval \"$(_JENKINSCTL_COMPLETE=zsh_source jenkinsctl)\"' >> ~/.zshrc")
        print("\n# Then reload your zsh configuration:")
        print("source ~/.zshrc")

    elif shell == "fish":
        print(
            "\n# To enable autocompletion for fish, add the following to your Fish config (~/.config/fish/config.fish):")
        print("echo 'eval (jenkinsctl enable-completion fish | source)' >> ~/.config/fish/config.fish")
        print("\n# Then reload your fish shell configuration:")
        print("source ~/.config/fish/config.fish")

    else:
        print("\n# Unsupported shell. Please specify bash, zsh, or fish.")
