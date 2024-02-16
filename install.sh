echo "~~~ install dependencies ~~~"
sudo apt install uhubctl git python3-pip python3-flask iptables python3-ua-parser
sudo cp motd /etc/motd
sudo cp motd_dynamic.sh /etc/profile.d/motd_dynamic.sh
sudo chmod +x /etc/profile.d/motd_dynamic.sh
echo "cd /opt/radiosilence" | sudo tee -a ~/.bashrc

echo "~~~ redirect requests on port 80 to 8080 ~~~~"
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080
echo iptables-persistent iptables-persistent/autosave_v4 boolean true | sudo debconf-set-selections
echo iptables-persistent iptables-persistent/autosave_v6 boolean true | sudo debconf-set-selections
sudo apt install -y iptables-persistent
sudo service iptables restart
sudo service ip6tables restart

echo "~~~ allow usb device access for non-root ~~~"
echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="1d6b", ATTR{idProduct}=="0003", MODE="0664", GROUP="plugdev"' | sudo tee /etc/udev/rules.d/99-usb.rules
echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="2109", ATTR{idProduct}=="3431", MODE="0664", GROUP="plugdev"' | sudo tee -a /etc/udev/rules.d/99-usb.rules
sudo udevadm control --reload-rules && sudo udevadm trigger
sudo usermod -a -G plugdev pi


echo "~~~ install service ~~~"
sudo cp -f radiosilence.service /lib/systemd/system/radiosilence.service
sudo chmod 644 /lib/systemd/system/radiosilence.service
sudo systemctl daemon-reload
sudo systemctl enable radiosilence.service
sudo service radiosilence start