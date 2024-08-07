{
  description = "GPT4all cli project";

  nixConfig = {
    bash-prompt = "\[ aicli \\w \]$ ";
  };

  inputs = {
    nixpkgs = {
      # Author's favorite nixpkgs
      url = "github:grwlf/nixpkgs/local17";
    };

    # litrepl = {
    #   url = "git+file:/home/grwlf/proj/litrepl.vim/";
    # };
  };

  outputs = { self, nixpkgs }:
    let
      defaults = (import ./default.nix) {
        pkgs = import nixpkgs { system = "x86_64-linux"; };
        revision = if self ? rev then self.rev else null;
      };
    in {
      packages = {
        x86_64-linux = defaults;
      };
      devShells = {
        x86_64-linux = {
          default = defaults.shell;
        };
      };
    };

}
