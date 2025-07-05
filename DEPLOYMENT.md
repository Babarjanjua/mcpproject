# 🚀 Deployment Guide - Multilingual Learning Path Generator

## **Prerequisites**
- ✅ OpenAI API key
- ✅ GitHub repository with your code
- ✅ Vercel account (free)
- ✅ Streamlit Cloud account (free)

---

## **Step 1: Environment Setup**

### **1.1 Create Environment File**
```bash
# Copy the template
cp env_template.txt .env

# Edit .env and add your OpenAI key
# Replace 'your_openai_api_key_here' with your actual OpenAI key
```

### **1.2 Your .env file should look like:**
```bash
OPENAI_API_KEY=sk-your-actual-openai-key-here
ENVIRONMENT=production
DEBUG=False
```

---

## **Step 2: Local Testing (CRITICAL)**

### **2.1 Run Local Tests**
```bash
# Test everything locally before deploying
python test_local.py
```

### **2.2 What the Tests Check:**
- ✅ **Environment Setup** - OpenAI API key and configuration
- ✅ **Backend API** - All endpoints working correctly
- ✅ **Frontend** - Streamlit app imports and dependencies
- ✅ **MCP Servers** - Server availability (if configured)
- ✅ **Integration** - Full workflow from search to learning path

### **2.3 If Tests Fail:**
- Install missing packages: `pip install -r requirements.txt`
- Check OpenAI API key in `.env` file
- Verify all files are in correct locations
- Fix any import or dependency issues

**⚠️ IMPORTANT: Do not proceed to deployment if local tests fail!**

---

## **Step 3: Deploy Backend to Vercel**

### **3.1 Install Vercel CLI**
```bash
npm install -g vercel
```

### **3.2 Login to Vercel**
```bash
vercel login
```

### **3.3 Deploy Backend**
```bash
# Option A: Using deployment script (recommended)
chmod +x deploy.sh
./deploy.sh

# Option B: Manual deployment
vercel --prod
```

### **3.4 Get Your Vercel URL**
After deployment, you'll get a URL like:
```
https://your-app-name.vercel.app
```

**Save this URL!** You'll need it for the frontend.

---

## **Step 4: Update Frontend Configuration**

### **4.1 Update Backend URL**
Edit `frontend/app.py` and change:
```python
# Change this line (around line 50)
BACKEND_URL = "http://localhost:8000"

# To your Vercel URL
BACKEND_URL = "https://your-app-name.vercel.app"
```

### **4.2 Commit and Push Changes**
```bash
git add .
git commit -m "Update backend URL for deployment"
git push origin main
```

---

## **Step 5: Deploy Frontend to Streamlit Cloud**

### **5.1 Go to Streamlit Cloud**
1. Visit [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"

### **5.2 Configure Your App**
- **Repository**: Select your GitHub repository
- **Branch**: `main`
- **Main file path**: `frontend/app.py`
- **App URL**: Leave as default (or customize)

### **5.3 Add Environment Variables (Optional)**
If you want to set environment variables in Streamlit Cloud:
- **Key**: `OPENAI_API_KEY`
- **Value**: Your OpenAI API key

### **5.4 Deploy**
Click "Deploy!" and wait for deployment to complete.

---

## **Step 6: Test Your Application**

### **6.1 Test Backend**
Visit your Vercel URL + `/docs`:
```
https://your-app-name.vercel.app/docs
```
You should see the FastAPI documentation.

### **6.2 Test Frontend**
Visit your Streamlit Cloud URL:
```
https://your-app-name.streamlit.app
```
You should see your application running.

### **6.3 Test Integration**
1. Go to your Streamlit app
2. Try searching for courses
3. Generate a learning path
4. Check if everything works

---

## **Step 7: Troubleshooting**

### **Common Issues:**

#### **Local Tests Failed**
- Check error messages from `python test_local.py`
- Install missing packages: `pip install -r requirements.txt`
- Verify OpenAI API key is correct
- Check Python version (3.8+ required)

#### **Backend Not Working**
- Check Vercel deployment logs
- Verify environment variables in Vercel dashboard
- Ensure `requirements.txt` is in root directory
- Test backend endpoints directly

#### **Frontend Can't Connect to Backend**
- Verify the backend URL in `frontend/app.py`
- Check CORS settings in backend
- Test backend endpoints directly
- Check Streamlit Cloud logs

#### **API Errors**
- Verify OpenAI API key is correct
- Check API key is set in environment variables
- Monitor API usage in OpenAI dashboard

---

## **Step 8: Production Configuration**

### **8.1 Set Environment Variables in Vercel**
1. Go to your Vercel dashboard
2. Select your project
3. Go to Settings → Environment Variables
4. Add:
   - `OPENAI_API_KEY`: Your OpenAI key
   - `ENVIRONMENT`: `production`
   - `DEBUG`: `false`

### **8.2 Set Environment Variables in Streamlit Cloud**
1. Go to your Streamlit Cloud dashboard
2. Select your app
3. Go to Settings → Secrets
4. Add your environment variables

---

## **🎉 Success!**

Your application is now live at:
- **Backend**: `https://your-app-name.vercel.app`
- **Frontend**: `https://your-app-name.streamlit.app`

### **Features Working:**
- ✅ Course search with real APIs
- ✅ AI-powered recommendations
- ✅ Learning path generation
- ✅ Progress tracking
- ✅ Quiz generation
- ✅ Multilingual support
- ✅ Local testing before deployment

---

## **Next Steps**

1. **Monitor Usage**: Check OpenAI API usage
2. **Add Analytics**: Set up monitoring
3. **Scale**: Add more features as needed
4. **Customize**: Modify UI and functionality

---

## **Why Local Testing is Important**

Testing locally before deployment:
- 🐛 **Prevents deployment failures** - Catch issues early
- 🔧 **Saves time** - Fix problems before they reach production
- 📡 **Verifies functionality** - Ensure everything works as expected
- 💾 **Tests integrations** - Confirm APIs and databases work
- 🚀 **Builds confidence** - Know your app works before going live

---

## **Support**

If you encounter issues:
1. **First**: Run `python test_local.py` for detailed diagnostics
2. Check the troubleshooting section above
3. Review deployment logs
4. Verify all environment variables are set
5. Test endpoints individually

**Your AI-powered learning platform is now live!** 🎓🚀 