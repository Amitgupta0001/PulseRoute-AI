from loader import DataLoader
from explorer import DataExplorer

loader = DataLoader().load()

DataExplorer.explore(loader.messages, "Messages")
DataExplorer.explore(loader.users, "Users")
DataExplorer.explore(loader.groups, "Groups")
DataExplorer.explore(loader.group_members, "Group Members")
DataExplorer.explore(loader.business_accounts, "Business Accounts")
DataExplorer.explore(loader.user_business_history, "User Business History")
DataExplorer.explore(loader.message_history, "Message History")
DataExplorer.explore(loader.message_events, "Message Events")
DataExplorer.explore(loader.images, "Images")
DataExplorer.explore(loader.voice_notes, "Voice Notes")
DataExplorer.explore(
    loader.daily_notification_summary,
    "Daily Notification Summary"
)
DataExplorer.explore(loader.sample_messages, "Sample Messages")