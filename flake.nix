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

      in
      {

        devShell = pkgsAllowUnfree.mkShell {
          buildInputs = with pkgsAllowUnfree; [
            gnumake            
            poetry
            python3
          ];

          shellHook = ''
            # TODO: documentar esse comportamento,
            # devo abrir issue no github do nixpkgs
            export TMPDIR=/tmp

            # O PyCharm ativa por padrão o ambiente virtual.
            # Esse comando cria o .venv caso não exista e
            # ativa o .venv.
            # Notar que pode haver dessincronia por conta de
            # um .venv desatualizado.
            test -f .venv/bin/activate || make poetry.install
            source .venv/bin/activate

            echo "Entering the nix devShell no income back"
          '';
        };
      });
}
