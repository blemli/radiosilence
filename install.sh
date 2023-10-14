sudo apt install uhubctl git python3-pip python3-flask
pip3 install requirements.txt
sudo cp motd /etc/motd
# redirect port 80 to 8080
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080
sudo cp -f radiosilence.service /lib/systemd/system/radiosilence.service
sudo chmod 644 /lib/systemd/system/radiosilence.service
sudo systemctl daemon-reload
sudo systemctl enable radiosilence.service
echo "cd /opt/radiosilence" | sudo tee -a ~/.bashrc
sudo service radiosilence start
