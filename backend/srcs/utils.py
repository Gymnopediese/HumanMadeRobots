

def order_user(user1, user2):
	if user1.username < user2.username:
		return user1, user2
	else:
		return user2, user1