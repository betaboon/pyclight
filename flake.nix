{
  description = "pyclight-flake";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs";
    flake-utils.url = "github:numtide/flake-utils";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.flake-utils.follows = "flake-utils";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, poetry2nix }:
    (flake-utils.lib.eachDefaultSystem (system:
      let
        # see https://github.com/nix-community/poetry2nix/tree/master#api for more functions and examples.
        inherit (poetry2nix.legacyPackages.${system}) mkPoetryApplication;
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        packages = {
          pyclight = mkPoetryApplication { projectDir = self; };
          default = self.packages.${system}.pyclight;
        };

        devShells.default = pkgs.mkShell {
          packages = [ poetry2nix.packages.${system}.poetry ];
        };
      })) // {

      overlays.default = final: prev: {
        pyclight = self.packages.${prev.system}.pyclight;
      };

    };
}
