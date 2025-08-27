# Google Calendar Setup Guide
## For Baby Photography Appointment Scheduler

This guide explains how to configure the system to work with **any Google Calendar**, not just the one owned by your Google Cloud Console API account.

## 🌐 **Calendar Access Options**

### **1. Primary Calendar (Default)**
- **Target**: `"primary"` - The main calendar of the authenticated user
- **Use Case**: When you want to schedule appointments in your own personal/business calendar
- **Access**: Full read/write access
- **Configuration**: `target_calendar_id: "primary"`

### **2. Any Calendar You Own**
- **Target**: Specific calendar ID (e.g., `"abc123@group.calendar.google.com"`)
- **Use Case**: When you want to schedule in a different calendar you own
- **Access**: Full read/write access
- **Configuration**: `target_calendar_id: "abc123@group.calendar.google.com"`

### **3. Shared/Team Calendars**
- **Target**: Calendar IDs of calendars shared with you
- **Use Case**: When working with a team or using a shared business calendar
- **Access**: Usually read/write if shared as a writer
- **Configuration**: `target_calendar_id: "team_calendar@group.calendar.google.com"`

### **4. Business/Organization Calendars**
- **Target**: Calendars within your Google Workspace organization
- **Use Case**: When using a business calendar managed by your organization
- **Access**: Depends on your organization's permissions
- **Configuration**: `target_calendar_id: "business@yourdomain.com"`

## 🔍 **How to Find Calendar IDs**

### **Method 1: Google Calendar Web Interface**
1. Go to [Google Calendar](https://calendar.google.com)
2. In the left sidebar, find the calendar you want to use
3. Click the three dots (⋮) next to the calendar name
4. Select "Settings and sharing"
5. Scroll down to "Integrate calendar"
6. Copy the "Calendar ID" (it will look like `abc123@group.calendar.google.com`)

### **Method 2: Calendar Settings**
1. In Google Calendar, click the three dots (⋮) next to any calendar
2. Select "Settings and sharing"
3. Look for "Calendar ID" in the settings
4. Copy the ID

### **Method 3: URL Method**
1. Open the calendar you want to use
2. Look at the URL in your browser
3. The calendar ID is in the URL: `https://calendar.google.com/calendar/u/0/r/cid/`**`CALENDAR_ID_HERE`**

## ⚙️ **Configuration Examples**

### **Example 1: Use Your Primary Calendar**
```yaml
calendar:
  target_calendar_id: "primary"  # Your main calendar
  timezone: "America/New_York"
  business_hours:
    start: "09:00"
    end: "17:00"
    days: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
```

### **Example 2: Use a Specific Business Calendar**
```yaml
calendar:
  target_calendar_id: "photography_studio@yourdomain.com"  # Specific calendar ID
  timezone: "America/New_York"
  business_hours:
    start: "09:00"
    end: "17:00"
    days: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
```

### **Example 3: Use a Shared Team Calendar**
```yaml
calendar:
  target_calendar_id: "team_schedule@group.calendar.google.com"  # Shared calendar
  timezone: "America/New_York"
  business_hours:
    start: "09:00"
    end: "17:00"
    days: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
```

### **Example 4: Use Multiple Calendars (Advanced)**
```yaml
calendar:
  target_calendar_id: "primary"  # Main calendar for appointments
  backup_calendars:  # Additional calendars for availability checking
    - "availability@yourdomain.com"
    - "blocked_times@yourdomain.com"
  timezone: "America/New_York"
  business_hours:
    start: "09:00"
    end: "17:00"
    days: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
```

## 🔐 **Permission Requirements**

### **For the Target Calendar, You Need:**
- **Read Access**: To check existing appointments and availability
- **Write Access**: To create, update, and delete appointments
- **Manage Access**: To set reminders and notifications

### **How to Grant Access:**
1. **If you own the calendar**: No additional setup needed
2. **If it's shared with you**: Ask the owner to grant "Make changes to events" permission
3. **If it's a business calendar**: Contact your Google Workspace administrator

## 🚀 **Setup Steps**

### **Step 1: Choose Your Target Calendar**
1. Decide which calendar you want to use for appointments
2. Get the calendar ID using one of the methods above
3. Note the timezone of the calendar

### **Step 2: Update Configuration**
1. Copy `config.example.yaml` to `config.yaml`
2. Edit the calendar section:
   ```yaml
   calendar:
     target_calendar_id: "YOUR_CALENDAR_ID_HERE"
     timezone: "YOUR_TIMEZONE"
   ```

### **Step 3: Test Access**
1. Run the setup command:
   ```bash
   python main.py --setup
   ```
2. The system will test access to your target calendar
3. Verify the calendar name and timezone are correct

### **Step 4: Verify Permissions**
1. Try creating a test appointment
2. Check that it appears in your target calendar
3. Verify that reminders and notifications work

## 🔧 **Advanced Calendar Configuration**

### **Multiple Calendar Support**
The system can be extended to work with multiple calendars:

```python
# In calendar_manager.py, you could add:
def check_availability_across_calendars(self, start_time, end_time):
    """Check availability across multiple calendars"""
    calendars = [self.calendar_id] + self.config.get('calendar.backup_calendars', [])
    
    for cal_id in calendars:
        if self._is_time_available(cal_id, start_time, end_time):
            return True
    return False
```

### **Calendar-Specific Settings**
You can configure different settings for different calendars:

```yaml
calendar:
  target_calendar_id: "primary"
  calendar_specific_settings:
    primary:
      business_hours:
        start: "09:00"
        end: "17:00"
      buffer_time: 15
    business:
      business_hours:
        start: "08:00"
        end: "18:00"
      buffer_time: 30
```

## ❓ **Common Questions**

### **Q: Can I use a calendar I don't own?**
**A**: Yes, as long as you have been granted write access to it. The calendar owner needs to share it with you and give you "Make changes to events" permission.

### **Q: What if the calendar is in a different timezone?**
**A**: The system will automatically handle timezone conversion. Set the `timezone` field in your config to match your business timezone, and the system will convert times appropriately.

### **Q: Can I schedule appointments in multiple calendars?**
**A**: Currently, the system targets one primary calendar, but this can be extended to support multiple calendars for different types of appointments.

### **Q: What happens if I lose access to the calendar?**
**A**: The system will show an error when trying to create or modify appointments. You'll need to either regain access or change the `target_calendar_id` to a calendar you do have access to.

### **Q: Can I use a calendar from a different Google account?**
**A**: Yes, as long as that calendar is shared with your authenticated account. You'll need to authenticate with the account that has access to the target calendar.

## 🎯 **Best Practices**

1. **Use a Dedicated Business Calendar**: Create a separate calendar specifically for your photography business
2. **Set Appropriate Permissions**: Ensure only necessary people have access to your business calendar
3. **Regular Backups**: Export your calendar data regularly as a backup
4. **Test Permissions**: Always test calendar access after making changes
5. **Monitor Usage**: Keep track of API usage to avoid hitting Google's limits

## 🔍 **Troubleshooting**

### **Error: "Calendar not found"**
- Verify the calendar ID is correct
- Ensure you have access to the calendar
- Check that the calendar hasn't been deleted

### **Error: "Insufficient permissions"**
- Ask the calendar owner to grant you write access
- Verify you're authenticated with the correct account
- Check if the calendar requires special permissions

### **Error: "Invalid calendar ID"**
- Make sure the calendar ID format is correct
- Remove any extra spaces or characters
- Try using "primary" for your main calendar

---

**The system is designed to work with any Google Calendar you have access to, making it flexible for different business setups and team configurations!** 🎯📅
