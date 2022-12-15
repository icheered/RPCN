import rosbag

try:
    bag = rosbag.Bag('data/run1.bag')

    print(f"Message count: {bag.get_message_count()}")
    print(f"Start time: {bag.get_start_time()}")
    print(f"End time: {bag.get_end_time()}")
    print(f"Duration: {bag.get_end_time() - bag.get_start_time()}")

    topics = list(bag.get_type_and_topic_info()[1].keys())
    print("Topics: ")
    for topic in topics:
        print(f"  - {topic}")


    for topic, msg, t in bag.read_messages(topics=['/imu/acceleration']):
        print(f"Topic: {topic}, Time: {t}, Message: {msg}")

except:
    print("An exception occurred")
finally:
    print("Closing bag")
    bag.close()

