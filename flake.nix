{
  description = "Flake do bb-wrapper";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let

        pkgsAllowUnfree = import nixpkgs {
          system = "x86_64-linux";
          config = { allowUnfree = true; };
        };

        config = {
          projectDir = ./.;
        };

        hack = pkgsAllowUnfree.writeShellScriptBin "hack" ''
          # Dont overwrite customised configuration
          if ! test -f .env; then
            make config.env
          fi

          # https://dev.to/ifenna__/adding-colors-to-bash-scripts-48g4
          echo -e '\n\n\n\e[32m\tAmbiente pronto!\e[0m\n'
          echo -e '\n\t\e[33mignore as proximas linhas...\e[0m\n\n\n'
        '';
      in
      {

        poetryEnv = import ./mkPoetryEnv.nix.nix {
          pkgs = nixpkgs.legacyPackages.${system};
        };

        env = pkgsAllowUnfree.poetry2nix.mkPoetryEnv config;

        devShell = pkgsAllowUnfree.mkShell {
          buildInputs = with pkgsAllowUnfree; [
            #(pkgsAllowUnfree.poetry2nix.mkPoetryEnv config)
            gnumake
            hack
            poetry
            python3
          ];

          shellHook = ''
            # TODO: documentar esse comportamento,
            # devo abrir issue no github do nixpkgs
            export TMPDIR=/tmp

            echo "Entering the nix devShell no income back"
            hack
          '';
        };
      });
}
