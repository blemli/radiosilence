# radiosilence
enforce radio silence during phone calls!

![radiosilence](assets/radiosilence.png)

## installation
```bash
cd /opt
sudo mkdir radiosilence
sudo chown pi radiosilence
git clone https://github.com/blemli/radiosilence && cd radiosilence
sudo chmod +x install.sh && ./install.sh

```

## usage
send a http get request to `http://<ip>/silent` to mute the speaker or `http://<ip>/loud` to un-mute it. You can Find the ip on "http://radiosilence.local/ip"

## on the phone
![2023-10-14_12-43-19](assets/2023-10-14_12-43-19.png)

## learned
yealink phone doesn't do mDNS. There is no useful way to do https in a local network, how sad.


## Development

### Release

```bash
gh release create vX.Y.Z --generate-notes --prerelease
```


## etymology
radio silence is a term used in the military to enforce a period of radio silence. It is used to prevent the enemy from intercepting messages. The term is also used in the context of radio broadcasting to refer to a period during which a station or network will not broadcast any programming.

