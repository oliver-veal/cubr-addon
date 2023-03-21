#!/bin/bash

set -e

semver=1.9.0

package_name=cubr

oses=("linux" "darwin" "windows")
archs=("amd64")

rm -rf bin
cp -r ../core/bin bin
rm -rf src/**/__pycache__
rm -rf src/__pycache__
rm -f src/cubr

dir=$(pwd)

for os in "${oses[@]}"; do
  for arch in "${archs[@]}"; do
    echo "Building for $os/$arch"

    cd $dir

    bin_dir="bin/$os/$arch"

    mkdir -p $bin_dir/cubr_addon

    mv $bin_dir/cubr $bin_dir/cubr_addon || true
    mv $bin_dir/cubr.exe $bin_dir/cubr_addon || true
    cp -r src/* $bin_dir/cubr_addon

    cd $bin_dir

    zip -r -9 $package_name.zip .
    
    wrangler r2 object put cubr-addon/v$semver/$os/$arch/$package_name.zip -f $package_name.zip
  done
done
