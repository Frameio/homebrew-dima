rm -f *.tar.gz
tar zcf dima-1.0.0.tar.gz ../dima.py ../sample_creds ../README.md ../deploy.sh
echo -n dima-1.0.0.tar.gz | shasum -a 256
