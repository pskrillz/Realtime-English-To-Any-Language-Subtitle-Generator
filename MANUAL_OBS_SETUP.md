# 🎥 Manual OBS Setup (Script Properties Not Working)

## 🚨 **If Script Properties Don't Show Up - Use This Method**

This happens when OBS can't load the Python script properly. Here's the manual setup that works 100% of the time.

---

## 🛠️ **Manual Text Source Setup**

### **Step 1: Create Text Source Manually**

1. **In OBS Sources panel, click `+`**
2. **Select:** `Text (FreeType 2)` or `Text (GDI+)`
3. **Name:** `Farsi_Subtitles`
4. **Click:** `OK`

### **Step 2: Configure Text Source**

**Text Properties:**
- **Text:** Leave blank (will be filled automatically)
- **Font:** Arial or Calibri
- **Size:** `48` (or larger for visibility)
- **Color:** White (`#FFFFFF`)
- **Background:** None (transparent)
- **Outline:** Yes, Black (`#000000`), Size: 4
- **Alignment:** Center

**Advanced Options:**
- **Read from file:** ✅ **CHECK THIS BOX**
- **Text File:** Browse to `C:\Coding\AI\Farsi Translator\subtitle.txt`
- **Chat log mode:** ❌ Unchecked
- **Use custom text extents:** ❌ Unchecked

### **Step 3: Position the Subtitles**

1. **Drag the text source** to bottom center of your video
2. **Or use Transform:**
   - Right-click → Transform → Edit Transform
   - **Position X:** `960` (for 1920px width)
   - **Position Y:** `900` (for 1080px height)
   - **Alignment:** Center

---

## 🌐 **Add YouTube Browser Source**

### **Step 1: Add Browser Source**
1. **In Sources panel, click `+`**
2. **Select:** `Browser`
3. **Name:** `YouTube_Video`
4. **Click:** `OK`

### **Step 2: Configure Browser**
- **URL:** `https://www.youtube.com`
- **Width:** `1920`
- **Height:** `1080`
- **FPS:** `30`
- **Custom CSS:** (leave blank)
- **Shutdown when not visible:** ✅ Checked
- **Refresh on scene change:** ✅ Checked

### **Step 3: Size Browser Source**
1. **Right-click browser source** → `Transform` → `Fit to Screen`
2. **Make sure it's below the subtitle source** in the source list

---

## 🧪 **Test the Setup**

### **Step 1: Test Subtitle Display**
1. **Open:** `C:\Coding\AI\Farsi Translator\subtitle.txt` in Notepad
2. **Type:** `تست زیرنویس فارسی`
3. **Save the file**
4. **In OBS:** You should see the Farsi text appear immediately

### **Step 2: Test with Flask Interface**
1. **Ensure Flask is running:** `http://localhost:5000`
2. **Click:** "🚀 Start Translation" 
3. **The subtitle.txt file should start updating automatically**
4. **OBS should display the updating subtitles**

---

## 🎬 **Complete Workflow**

### **Setup Phase (One Time):**
1. ✅ Create text source reading from `subtitle.txt`
2. ✅ Add browser source for YouTube
3. ✅ Position subtitles at bottom center
4. ✅ Test with manual text in `subtitle.txt`

### **Usage Phase (Every Time):**
1. **Start Flask:** `python flask_web_interface.py`
2. **Open Flask interface:** `http://localhost:5000`
3. **Start translation:** Click 🚀 button
4. **Open OBS:** Your configured scene
5. **Navigate to YouTube:** In browser source
6. **Play English video:** Watch Farsi subtitles appear!

---

## 🔧 **Advanced Manual Setup**

### **Multiple Subtitle Styles**
Create different text sources for different purposes:

**For Movies:**
- Font Size: 52
- Color: White with thick black outline
- Position: Bottom center

**For News:**
- Font Size: 44
- Color: Yellow with black outline  
- Position: Lower third

**For Streaming:**
- Font Size: 36
- Color: Cyan with dark outline
- Position: Top or side

### **Background Box (Optional)**
1. **Add:** Color Source
2. **Make it:** Semi-transparent black rectangle
3. **Position:** Behind subtitle text
4. **Size:** Slightly larger than text area

---

## 🔍 **Troubleshooting Manual Setup**

### **Problem: Subtitles not appearing**
**Check:**
- ✅ "Read from file" is checked
- ✅ File path points to correct subtitle.txt
- ✅ Text source is above browser source in list
- ✅ subtitle.txt file exists and has content

### **Problem: Subtitles not updating**
**Check:**
- ✅ Flask interface is running and translating
- ✅ subtitle.txt file is being written to
- ✅ File permissions allow OBS to read the file
- ✅ No other program has the file locked

### **Problem: Text looks bad**
**Adjust:**
- Increase outline size (4-6 pixels)
- Use different font (Arial, Calibri, or Tahoma)
- Add semi-transparent background
- Increase font size for better readability

---

## 📊 **File Monitoring**

**You can verify the system is working by watching these files:**

```bash
# Watch subtitle.txt update in real-time
tail -f subtitle.txt

# Check if Flask is generating translations
curl http://localhost:5000/stats
```

---

## 🎉 **Success Indicators**

**Manual setup is working when:**
- ✅ OBS shows YouTube video playing
- ✅ Text source displays content from subtitle.txt
- ✅ Subtitles update when subtitle.txt changes
- ✅ Flask interface shows active translation
- ✅ Real-time Farsi subtitles appear during English video

---

## 🚀 **Why This Works Better**

**Manual setup advantages:**
- ✅ **100% Compatible:** Works with all OBS versions
- ✅ **No Python Dependencies:** Doesn't require OBS Python
- ✅ **More Reliable:** Direct file reading
- ✅ **Easier Debugging:** Can test each component separately
- ✅ **Full Control:** Customize exactly how you want

**This manual method is actually more reliable than the Python script!** 