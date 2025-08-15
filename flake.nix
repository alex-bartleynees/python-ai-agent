{
  description = "A Nix-flake-based Python development environment";
  inputs.nixpkgs.url = "https://flakehub.com/f/NixOS/nixpkgs/0.1.*.tar.gz";
  outputs = { self, nixpkgs }:
    let
      supportedSystems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forEachSupportedSystem = f: nixpkgs.lib.genAttrs supportedSystems (system: f {
        pkgs = import nixpkgs { inherit system; };
      });
    in
    {
      devShells = forEachSupportedSystem ({ pkgs }: {
        default = pkgs.mkShell {
          packages = with pkgs; [ 
            uv
            python311
          ] ++
            (with pkgs.python311Packages; [
              pip
              pylint
            ]);
            
          shellHook = ''
            echo "Development environment with uv and Python 3.10+"
            echo "Python version: $(python --version)"
            echo "uv version: $(uv --version)"
            echo ""
            echo "Run 'uv sync' to install dependencies"
          '';
        };
      });
    };
}
