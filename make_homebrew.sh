# Makes the tarball for homebrew, outputs the new sha

# Usage:
# ./make.sh 1.0.0

rm -f dima-*.tar.gz
tar zcf dima-$1.tar.gz dima.py sample_creds README.md deploy.sh setup.py
shasum -a 256 dima-$1.tar.gz 
