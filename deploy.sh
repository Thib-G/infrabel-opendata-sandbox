npm run build
scp -r ./dist infrabel-opendata.goelff.be:~/tmp/infrabel-opendata.goelff.be
ssh infrabel-opendata.goelff.be "chmod -R u+rw-x,go+r-wx,ugo+X ~/tmp/infrabel-opendata.goelff.be && rm -r -f /var/www/infrabel-opendata.goelff.be/public_html/* && mv ~/tmp/infrabel-opendata.goelff.be/* /var/www/infrabel-opendata.goelff.be/public_html && rm -r ~/tmp/infrabel-opendata.goelff.be && exit"
