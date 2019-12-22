import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import cv2
from PIL import Image, ImageTk
from stegano import lsb,lsbset,red, steganalysis
from stegano.lsbset import generators
import inspect
from DCT import DCT
# import ScrollableFrame as sf

from LSBSteg import LSBSteg

container2wt = 0

def select_image():
    print('Select Image')
    global image_path
    image_path = tk.filedialog.askopenfilename(title="Select image", filetypes=[("all files", '*.*')])
    print(image_path)
    if (image_path):
        root.update_idletasks()
        global original_image_label
        load = Image.open(image_path)
        original_image = ImageTk.PhotoImage(load)
        print(type(original_image))
        original_image_label.config(image = original_image)
        original_image_label.image = original_image
        original_image_label.pack(in_=container2, fill=tk.BOTH, expand=True)

def select_secret_file():
    # global secret_image_path
    print("Select secret file")
    secret_file = tk.filedialog.askopenfile(title="Select file", filetypes=[("All files", '*.*')])
    # print(secret_image_path)
    data = secret_file.read()
    text1.insert(tk.END, data)

def clear_image():
    print('Save Image')
    # print(processed_image_label.image)
    clear_processed_image()

def exit_app():
    print('Exit App')
    messagebox = tk.messagebox.askyesno("Exit Application","Are you sure you want to exit?")
    print(messagebox)
    if (messagebox):
        root.quit()

def process():
    try:
        print('process()')
        encrypt_decrypt = options_clicked.get()
        algo_technique = technique_options_clicked.get()
        # Check for secret data
        secret_string = text1.get("1.0",tk.END)
        # check for carrier
        try: image_path
        except NameError:
            tk.messagebox.showwarning("Data Required","Please select carrier image to proceed")
            return
        # original_image = cv2.imread(image_path)
        print(secret_string)
        if (algo_technique == technique_options[0]):
            # LSB Algorithm
            lsbAlgoDefault(encrypt_decrypt, secret_string)
        elif (algo_technique == technique_options[1]):
            # stegano plain
            lsbAlgoStegano("Plain",secret_string,encrypt_decrypt)
        elif (algo_technique == technique_options[2]):
            # stegano plain
            lsbAlgoStegano("Eratosthenes", secret_string, encrypt_decrypt)
        elif (algo_technique == technique_options[3]):
            # stegano plain
            lsbAlgoStegano("Carmichael", secret_string, encrypt_decrypt)
        elif (algo_technique == technique_options[4]):
            # stegano plain
            lsbAlgoStegano("Composite", secret_string, encrypt_decrypt)
        elif (algo_technique == technique_options[5]):
            # stegano plain
            lsbAlgoStegano("Fermat", secret_string, encrypt_decrypt)
        elif (algo_technique == technique_options[6]):
            # stegano plain
            lsbAlgoStegano("Fibonacci", secret_string, encrypt_decrypt)
        elif (algo_technique == technique_options[7]):
            # stegano plain
            lsbAlgoStegano("Ackermann", secret_string, encrypt_decrypt)
        elif (algo_technique == technique_options[8]):
            # stegano plain
            lsbAlgoStegano("log_gen", secret_string, encrypt_decrypt)
        elif (algo_technique == technique_options[9]):
            # stegano plain
            lsbAlgoStegano("Mersenne", secret_string, encrypt_decrypt)
        elif (algo_technique == technique_options[10]):
            # stegano plain
            lsbAlgoStegano("Red", secret_string, encrypt_decrypt)
        elif (algo_technique == technique_options[11]):
            # stegano plain
            lsbAlgoStegano("DCT", secret_string, encrypt_decrypt)
    except NameError as error:
        print(error)

def lsbAlgoStegano(type, secret_string, encrypt_decrypt):
    if (encrypt_decrypt == options[0]):
        if (len(secret_string) == 1):
            print("Empty Secret:: Showing warning")
            tk.messagebox.showwarning("Data Required", "Please enter secret data to be encoded")
            return
    if (type == "Plain"):
        if (encrypt_decrypt == options[0]):
            secret = lsb.hide(image_path, secret_string)
            secret.save("secret/secret.png")
            displayImage("secret/secret.png")
        else:
            secret = lsb.reveal(image_path)
            displaySecret(secret)
            saveSecretToFile(secret)
    elif (type == "Red"):
        if (encrypt_decrypt == options[0]):
            secret = red.hide(image_path, secret_string)
            secret.save("secret/secret.png")
            displayImage("secret/secret.png")
        else:
            secret = red.reveal(image_path)
            displaySecret(secret)
            saveSecretToFile(secret)
    elif (type == "DCT"):
        if (encrypt_decrypt == options[0]):
            outFile = "secret/secretDCT.png"
            x = DCT(image_path)
            secret = x.DCTEn(secret_string, outFile)
            print("secret :: DCT:: ",secret)
            # secret = red.hide(image_path, secret_string)
            # secret.save("secret.png")
            displayImage("secret/secretDCT.png")
        else:
            y = DCT(image_path)
            secret = y.DCTDe()
            # secret = red.reveal(image_path)
            displaySecret(secret)
            saveSecretToFile(secret)
    else:
        gen_method = None
        if (type == "Eratosthenes"):
            gen_method = generators.eratosthenes()
        elif (type == "Carmichael"):
            gen_method = generators.carmichael()
        elif (type == "Composite"):
            gen_method = generators.composite()
        elif (type == "Fermat"):
            gen_method = generators.fermat()
        elif (type == "Fibonacci"):
            gen_method = generators.fibonacci()
        elif (type == "Ackermann"):
            gen_method = generators.ackermann(3)
        elif (type == "log_gen"):
            gen_method = generators.log_gen()
        elif (type == "Mersenne"):
            gen_method = generators.mersenne()

        if (encrypt_decrypt == options[0]):
            secret = lsbset.hide(image_path, secret_string,gen_method)
            secret.save("secret/secret.png")
            displayImage("secret/secret.png")
        else:
            secret = lsbset.reveal(image_path,gen_method)
            displaySecret(secret)
            saveSecretToFile(secret)


def saveImage():
    print("af")

def saveSecretToFile(secret):
    print("saveSecretToFile")
    f = tk.filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    if f is None:
        return
    text2save = str(secret)
    f.write(text2save)
    f.close()


def lsbAlgoDefault(encrypt_decrypt, secret_string):
    # if (algo_technique == technique_options[0]):
        # LSB:: Text Steganography
        if (encrypt_decrypt == options[0]):
            print("LSB:::Text::: Encrypt")
            # Warning for secret string
            if (len(secret_string) == 1):
                print("Empty Secret:: Showing warning")
                tk.messagebox.showwarning("Data Required", "Please enter secret data to be encoded")
                return
            # encoding
            steg = LSBSteg(cv2.imread(image_path))
            img_encoded = steg.encode_text(secret_string)
            cv2.imwrite("secret/secret.png", img_encoded)
            displayImage("secret/secret.png")
        else:
            print("LSB:::Text::: Decrypt")
            # decoding
            print(image_path)
            im = cv2.imread(image_path)
            steg = LSBSteg(im)
            displaySecret(steg.decode_text())
            print("Text value:", steg.decode_text())
    # else:
    #     if (encrypt_decrypt == options[0]):
    #         print("LSB:::Image::: Encrypt")
    #         # Warning for secret string
    #         if (len(secret_string) == 1):
    #             print("No secret image file selected")
    #             tk.messagebox.showwarning("Data Required", "Please select secret img file to be encoded")
    #             return
    #         # encoding
    #         print(image_path)
    #         print(secret_image_path)
    #         img1 = cv2.imread(image_path)
    #         print(type(img1))
    #         steg = LSBSteg(img1)
    #         img = cv2.imread(secret_image_path)
    #         print(type(img))
    #         new_im = steg.encode_image(img)
    #         displayImage(new_im)
    #         cv2.imwrite("C:/Users/Justin2805/Downloads/new_image.png", new_im)
    #     else:
    #         print("LSB:::Image::: Decrypt")
    #         # decoding
    #         print(image_path)
    #         steg = LSBSteg(image_path)
    #         orig_im = steg.decode_image()
    #         displayImage(orig_im)


def displayImage(path):
    print(type(path))
    # im = Image.fromarray(image)
    global processed_image_label
    # processed_image = ImageTk.PhotoImage(image=im)
    # print(type(processed_image))
    load = Image.open(path)
    processed_image = ImageTk.PhotoImage(load)
    processed_image_label.config(image=processed_image)
    processed_image_label.image = processed_image
    processed_image_label.pack(in_=container4, fill=tk.BOTH, expand=True)

def displaySecret(secret):
    clear_processed_image()
    global processed_image_label
    processed_image_label.config(text=secret)
    # processed_image_label.image = processed_image
    processed_image_label.pack(in_=container4, fill=tk.BOTH, expand=True)

def clear_processed_image():
    print("clear image")
    processed_image_label.config(image='')
    processed_image_label.pack(in_=container4, fill=tk.BOTH, expand=True)

def clear_text_description():
    print("clear image")
    text2.delete('1.0', tk.END)

def technique_callback(*args):
    clear_text_description()
    all_generators = inspect.getmembers(generators, inspect.isfunction)
    option = technique_options_clicked.get()
    print("technique_callback: ", option)
    data = ""
    if (option == technique_options[0]):
        data ="Technique 1\nLSB is the lowest bit in a series of numbers in binary. e.g. in the binary number: 10110001, the least significant bit is far right 1.\n" \
              "The LSB  based Steganographyis one of the steganographic methods,  used  to  embed  the  secret  data  in  to  the  least significant bits of the " \
              "pixel values in a cover image. e.g. 240 can be hidden in the first eight bytes of three pixels in a 24 bit image."
    elif (option == technique_options[1]):
        data ="Technique 2\nLSB is the lowest bit in a series of numbers in binary. e.g. in the binary number: 10110001, the least significant bit is far right 1.\n" \
              "The LSB  based Steganographyis one of the steganographic methods,  used  to  embed  the  secret  data  in  to  the  least significant bits of the " \
              "pixel values in a cover image. e.g. 240 can be hidden in the first eight bytes of three pixels in a 24 bit image."
    elif (option == technique_options[2]):
        data = "Generate the prime numbers with the sieve of Eratosthenes.\nhttps://oeis.org/A000040"
    elif (option == technique_options[3]):
        data = "Composite numbers n such that a^(n-1) == 1 (mod n)forevery a coprimeto n.\nhttps://oeis.org/A002997"
    elif (option == technique_options[4]):
        data = "Generate the composite numbers using the sieve of Eratosthenes.\nhttps://oeis.org/A002808"
    elif (option == technique_options[5]):
        data = "Generate the n-th Fermat Number.\nhttps://oeis.org/A000215"
    elif (option == technique_options[6]):
        data = "Generate the sequence of Fibonacci.\nhttps://oeis.org/A000045"
    elif (option == technique_options[7]):
        data = "Ackermann number"
    elif (option == technique_options[8]):
        data = "Logarithmic generator."
    elif (option == technique_options[9]):
        data = "Generate 2^p - 1, where p is prime.\nhttps://oeis.org/A001348"
    elif (option == technique_options[10]):
        data = "Hide and reveal a text message with the red portion of a pixel.\nFor example the pixel P1 = (R, G, B) will become P1' = (ord(ascii_character), G, B)." \
               "We are working at the byte level. "
    elif (option == technique_options[11]):
        data = "DCT   coefficients   are   used   for   JPEG   compression.   It separates  the  image  into  parts  of  differing  importance.  " \
               "It transforms a signal or image from the spatial domain to the frequency  domain.  It  can  separate  the  image  into  high, middle and low frequency " \
               "components. \n" \
               "Signal  energy  lies  at  low  frequency  in  image;  it  appears  in the  upper  left  corner  of  the  DCT.  Compression  can  be achieved   since   " \
               "the   lower   right   values   represent   higher frequencies,  and  generally  small  enough  to  be  neglected with little visible distortion. " \
               "DCT is used in steganography as- \n  1. Image is broken into 8×8 blocks of pixels. \n  2. Working from left to right, top to bottom, the DCT is applied to each block." \
               " \n  3. Each  " \
               "block  is  compressed  through  quantization table  to  scale  the  DCT  coefficients  and  message  is embedded in DCT coefficients."
    text2.insert(tk.END, data)
    print(data)

root = tk.Tk()
root.geometry("600x400")
root.title("Image Steganography")

top = tk.Frame(root, borderwidth=1,relief="solid")
top1 = tk.Frame(root, borderwidth=1,relief="solid")
bottom = tk.Frame(root, borderwidth=1,relief="solid")
left = tk.Frame(root, borderwidth=1, relief="solid")
right = tk.Frame(root, borderwidth=1, relief="solid")
container1 = tk.Frame(left, borderwidth=1, relief="solid")
container2 = tk.Frame(left, borderwidth=1, relief="solid")
container3 = tk.Frame(right, borderwidth=1, relief="solid")
container4 = tk.Frame(right, borderwidth=1, relief="solid")

secret_label = tk.Label(container1, text="Enter secret")
# original_img_label = tk.Label(container2, text="Original Image")
description_label = tk.Label(container3, text="Description")
# processed_img_label = tk.Label(container4, text="Processed Image")

top.pack(side="top", expand=False, fill="both")
top1.pack(side="top", expand=False, fill="both")
bottom.pack(side="bottom", expand=False, fill="both")
left.pack(side="left", expand=True, fill="both")
right.pack(side="right", expand=True, fill="both")
container1.pack(expand=False, fill="both", padx=5, pady=5)
container2.pack(expand=False, fill="both", padx=5, pady=5)
container3.pack(expand=False, fill="both", padx=5, pady=5)
container4.pack(expand=False, fill="both", padx=5, pady=5)

container2wt = container2.winfo_width()
print(container2wt)
original_image_label = tk.Label(root, width=container2wt)
processed_image_label = tk.Label(root, width=container2wt)

secret_label.pack()
# original_img_label.pack()
description_label.pack()
# processed_img_label.pack()


# Buttons
select_img_btn = tk.Button(root,text='Select Image', width=35, command=select_image)
select_img_btn.pack(in_=top, side="left")

select_secret_img_btn = tk.Button(root,text='Select secret file', width=35, command=select_secret_file)
select_secret_img_btn.pack(in_=top1, side="left")

clear_btn = tk.Button(root,text='Clear Image', width=35, command=clear_image)
clear_btn.pack(in_=bottom, side="left")

exit_btn = tk.Button(root,text='Exit App', width=35, command=exit_app)
exit_btn.pack(in_=bottom, side="right")

process_btn = tk.Button(root,text='Process', width=35, command=process)
process_btn.pack(in_=top, side="right")

# Drop down menu
options = [
    "Encrypt",
    "Decrypt"
]
technique_options = [
    "LSB Algorithm - Default",
    "LSB Algorithm - Plain",
    "LSB Algorithm : set - Eratosthenes",
    "LSB Algorithm : set - Carmichael",
    "LSB Algorithm : set - Composite",
    "LSB Algorithm : set - Fermat",
    "LSB Algorithm : set - Fibonacci",
    "LSB Algorithm : set - Ackermann",
    "LSB Algorithm : set - Log Gen",
    "LSB Algorithm : set - Mersenne",
    "LSB Algorithm : Red",
    "DCT"
]

options_clicked = tk.StringVar()
options_clicked.set(options[0])
technique_options_clicked = tk.StringVar()
technique_options_clicked.trace("w",technique_callback)
technique_options_clicked.set(technique_options[0])


drop = tk.OptionMenu(root, options_clicked, *options)
drop.pack(in_=top, anchor="n", side="bottom")
technique_drop = tk.OptionMenu(root, technique_options_clicked, *technique_options)
technique_drop.pack(in_=top1, anchor="n", side="bottom")

# textbox and scrollbar
text1 = tk.Text(root, width=35, height=5)
text2 = tk.Text(root, width=35, height=5)
scrollbar1 = tk.Scrollbar(root)
scrollbar2 = tk.Scrollbar(root)
scrollbar1.config(command=text1.yview)
scrollbar2.config(command=text2.yview)
text1.config(yscrollcommand=scrollbar1.set)
text2.config(yscrollcommand=scrollbar2.set)
scrollbar1.pack(in_=container1, side=tk.RIGHT, fill=tk.Y)
scrollbar2.pack(in_=container3, side=tk.RIGHT, fill=tk.Y)
text1.pack(in_=container1, side=tk.LEFT, fill=tk.BOTH, expand=True)
text2.pack(in_=container3, side=tk.LEFT, fill=tk.BOTH, expand=True)

all_generators = inspect.getmembers(generators, inspect.isfunction)
for generator in all_generators:
    print(generator[0], generator[1].__doc__)

root.mainloop()