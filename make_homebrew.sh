# Makes the tarball for homebrew, outputs the new sha

# Usage:
# ./make.sh 1.0.0

rm -f v*.tar.gz

# homebrew requires the tarball to have an interal folder
mkdir dima-$1
cp dima.py {sample_creds,README.md,deploy.sh,setup.py,LICENSE} dima-$1/
tar zcf v$1.tar.gz dima-$1
rm -rf dima-$1

shasum -a 256 v$1.tar.gz 
