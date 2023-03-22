from PIL import Image

# replacing 3 LSB of B with 3 MSB of a
def lsb_code(A: int, B: int) -> int:
	a = A >> 5
	b = B & 248
	C = b + a
	return C

def lsb_decode(C: int) -> int:
	a = C & 7
	A = a << 5
	return A

#Step 1
# image = Image.open("dice.png")

# r, g, b, a = image.split()
# data_r = list(r.getdata())
# data_g = list(g.getdata())
# data_b = list(b.getdata())
# data_a = list(a.getdata())
# image.save("dice.png")

# Step 2
def code_picture(picture: Image, message: str) -> Image:
	if picture.mode == "RGBA":
		r, g, b, a = picture.split()
	else:
		r, g, b = picture.split()
	data_r = list(r.getdata())
	data_g = list(g.getdata())
	data_b = list(b.getdata())
	if len(message) > 265 or len(message) > len(data_r)-1:
		print("Try shorter msg")
		return 
	data_r[0] = lsb_code(len(message), data_r[0])
	data_g[0] = lsb_code(len(message) << 3, data_g[0])
	data_b[0] = lsb_code(len(message) << 6, data_b[0])

	i = 1
	for c in message:
		data_r[i] = lsb_code(ord(c), data_r[i])
		data_g[i] = lsb_code(ord(c)<<3, data_g[i])
		data_b[i] = lsb_code(ord(c)<<6, data_b[i])
		i+=1
		r.putdata(data_r)
		g.putdata(data_g)
		b.putdata(data_b)
	if picture.mode == "RGBA":
		new_pic = Image.merge(picture.mode, (r, g, b, a))
	else:
		new_pic = Image.merge(picture.mode, (r, g, b))
	return new_pic

# Step 3
def decode_picture(picture: Image) -> str:
	if picture.mode == "RGBA":
		r, g, b, a = picture.split()
	else:
		r, g, b = picture.split()
	data_r = list(r.getdata())
	data_g = list(g.getdata())
	data_b = list(b.getdata())
	len_message = lsb_decode(data_r[0])+(lsb_decode(data_g[0])>>3)+(lsb_decode(data_b[0])>>6)
	message = []
	for i in range(1, len_message+1):
		c = chr(lsb_decode(data_r[i])+(lsb_decode(data_g[i])>>3)+(lsb_decode(data_b[i])>>6))
		# print(c)
		message.append(c)
	return "".join(message)

msg_str = "Be urself other already exist"
msg_img = Image.open("./assets/dice.png")
imgWithMsg = code_picture(msg_img,msg_str)
imgWithMsg.save("./results/dice_en.png")
print("mode: ", Image.open("./results/dice_en.png").mode)
st = decode_picture(Image.open("./results/dice_en.png"))
print(st)