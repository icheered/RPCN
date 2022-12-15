import rosbag




bag = rosbag.Bag('data/test1.bag')


print(f"Message count: {bag.get_message_count()}")
print(f"Start time: {bag.get_start_time()}")
print(f"End time: {bag.get_end_time()}")

print(f"Topics: {bag.get_type_and_topic_info()[1].keys()}")

bag.close()