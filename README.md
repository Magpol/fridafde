# FRiDA FDE bruteforce

Here's a small write-up on How-To use FRiDA to bruteforce Secure Startup with FDE-encryption on a Samsung G935F running Android 8.

![ExampleImage](/fde_example.png?raw=true "Title")

FRiDA requires a rooted device (or FRiDA injected into a specific process ). I won't go into details on how to accomplish this, just google ENG-ROOT or Magisk and you will probably
find a rooting solution that works for you. I've also included a small script to upload and start FRiDA on the connected device: startFrida.sh.

First of all, what are we doing? And why are we doing this? What i wanted to do is find a way of testing codes without hitting the limit of maximum password attempts. If the maximum attempt value is reached, the device will reboot and wipe. So my first step was to find out the processes or functions that managed all this.

From reading Android source and using Objection (another great tool) I soon figured out that  "android.os.storage.IStorageManager::decryptStorage" running in the process "com.android.settings:CryptKeeper" was the target for my FRiDA-script. I also knew from before that Vold is involved in the process of verifying and updating the crypto footer.
After some fiddling with Radare2 and FRiDA, I came to the conclusion that by replacing the "footer_put" function in Vold I could try codes and keep the counter at the original value.

Included are two different Python scripts:

The file "hooking-vold.py" replaces "footer_put" in Vold.
The file "hooking-mount.py" creates the RPC we use from the python script to try the different codes.

We need to run the files at the same time, in two different terminals.

How to use it:

1. Run "startFrida.sh" to upload and start frida server on your connected device.
2. Run "python3 hooking-vold.py" in a separate terminal.
3. Run "python3 hooking-mount.py" in main terminal.
4. Sometimes when the correct code is found, the process hangs the device. Just issue "adb reboot" to restart secure startup and then enter the correct code.
