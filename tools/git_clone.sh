cd github

git clone --bare https://github.com/MinxZ/D3Q.git

cd D3Q.git
git push --mirror https://github.com/MinxZ/BDQ.git

cd ..
rm -rf D3Q.git
