#!/bin/sh

# KISS shellscript to quickly test plugin without ruindtrip to github first
# (to run properly, it has to live in ${packages} sans package-metadata.json --
# lest ST3 rightfully kill the whole folder as a potential orphaned package)

rm -rf ~/temp/Normalise_Indentation_with_extra_crap
mkdir -p ~/temp/Normalise_Indentation_with_extra_crap
cp -r * ~/temp/Normalise_Indentation_with_extra_crap

rm ~/temp/Normalise_Indentation_with_extra_crap/Normalise-Indentation.sublime-project
rm ~/temp/Normalise_Indentation_with_extra_crap/Normalise-Indentation.sublime-workspace
rm ~/temp/Normalise_Indentation_with_extra_crap/test-build.sh
rm ~/temp/Normalise_Indentation_with_extra_crap/package-metadata.json

rm -rf ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/Normalise-Indentation
sleep 1s
mv ~/temp/Normalise_Indentation_with_extra_crap ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/Normalise-Indentation

echo "Upped installed version."