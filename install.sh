sudo apt install uhubctl git python3-pip python3-flask iptables
sudo cp motd /etc/motd
echo "cd /opt/radiosilence" | sudo tee -a ~/.bashrc
echo "~~~ redirect requests on port 80 to 8080 ~~~~"
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080
echo iptables-persistent iptables-persistent/autosave_v4 boolean true | sudo debconf-set-selections
echo iptables-persistent iptables-persistent/autosave_v6 boolean true | sudo debconf-set-selections
sudo apt install -y iptables-persistent
echo "~~~ install service ~~~"
sudo cp -f radiosilence.service /lib/systemd/system/radiosilence.service
sudo chmod 644 /lib/systemd/system/radiosilence.service
sudo systemctl daemon-reload
sudo systemctl enable radiosilence.service
sudo service radiosilence start
