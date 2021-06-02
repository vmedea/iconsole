# iconsole

Reverse engineering of the iconsole+ bike computer serial protocol, adapted for some Bluetooth LE devices.

Based on Harald Hoyer's [iconsole](https://github.com/haraldh/iconsole) and discussion [here](https://github.com/haraldh/iconsole/issues/2).

## Requirements

```
$ pip install -r --user requirements.txt
```

## Usage

Usage:

```
$ python3 main.py <macaddr> <sessionlog>
```

You can get the macaddr of the iconsole device using

```
$ hcitool -i hci0 lescan
```

Usually the device you're looking for will have a recognizable description.
