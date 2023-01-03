def collision_detection(object1, object2, accuracy = 1, object1BottomOnly = False, object1NegativeBuffer = 0, object2NegativeBuffer = 0):
    # Treat comments as headers
    # Object1 is the object whose corners are being tested
    # Object2 is the object being hit

    if not object1BottomOnly and accuracy >= 1:
        # First two are top left corner of Object1, then they move clockwise
        # Final test is center

        if (object2.position[0] + object2NegativeBuffer <= object1.position[0] + object1NegativeBuffer <= object2.position[0] + object2.width - object2NegativeBuffer and \
            object2.position[1] + object2NegativeBuffer <= object1.position[1] + object1NegativeBuffer <= object2.position[1] + object2.height - object2NegativeBuffer or \
                # Top Right (below)
            object2.position[0] + object2NegativeBuffer <= object1.position[0] + object1.width - object1NegativeBuffer <= object2.position[0] + object2.width - object2NegativeBuffer and \
            object2.position[1] + object2NegativeBuffer <= object1.position[1] + object1NegativeBuffer <= object2.position[1] + object2.height - object2NegativeBuffer or \
                # Bottom Right (below)
            object2.position[0] + object2NegativeBuffer <= object1.position[0] + object1.width - object1NegativeBuffer <= object2.position[0] + object2.width - object2NegativeBuffer and \
            object2.position[1] + object2NegativeBuffer <= object1.position[1] + object1.height - object1NegativeBuffer <= object2.position[1] + object2.height - object2NegativeBuffer or \
                # Bottom Left (below)
            object2.position[0] + object2NegativeBuffer <= object1.position[0] + object1NegativeBuffer <= object2.position[0] + object2.width - object2NegativeBuffer and \
            object2.position[1] + object2NegativeBuffer <= object1.position[1] + object1.height - object1NegativeBuffer <= object2.position[1] + object2.height - object2NegativeBuffer or \
                # Center Center
            object2.position[0] + object2NegativeBuffer <= object1.position[0] + (object1.width / 2) <= object2.position[0] + object2.width - object2NegativeBuffer and \
            object2.position[1] + object2NegativeBuffer <= object1.position[1] + (object1.height / 2) <= object2.position[1] + object2.height - object2NegativeBuffer):

            return True

        if accuracy >= 2:
        # First two are top center of Object1, then they move clockwise

            if (object2.position[0] + object2NegativeBuffer <= object1.position[0] + (object1.width / 2) <= object2.position[0] + object2.width - object2NegativeBuffer and \
                object2.position[1] + object2NegativeBuffer <= object1.position[1] + object1NegativeBuffer <= object2.position[1] + object2.height - object2NegativeBuffer or \
                    # Center Right (below)
                object2.position[0] + object2NegativeBuffer <= object1.position[0] + object1.width - object1NegativeBuffer <= object2.position[0] + object2.width - object2NegativeBuffer and \
                object2.position[1] + object2NegativeBuffer <= object1.position[1] + (object1.height / 2) <= object2.position[1] + object2.height - object2NegativeBuffer or \
                    # Bottom Center (below)
                object2.position[0] + object2NegativeBuffer <= object1.position[0] + (object1.width / 2) <= object2.position[0] + object2.width - object2NegativeBuffer and \
                object2.position[1] + object2NegativeBuffer <= object1.position[1] + object1.height - object1NegativeBuffer <= object2.position[1] + object2.height - object2NegativeBuffer or \
                    # Center Left (below)
                object2.position[0] + object2NegativeBuffer <= object1.position[0] + object1NegativeBuffer <= object2.position[0] + object2.width - object2NegativeBuffer and \
                object2.position[1] + object2NegativeBuffer <= object1.position[1] + (object1.height / 2) <= object2.position[1] + object2.height - object2NegativeBuffer):
            
                return True

    elif object1BottomOnly and \
        (object2.position[0] + object2NegativeBuffer <= object1.position[0] + object1.width - object1NegativeBuffer <= object2.position[0] + object2.width - object2NegativeBuffer and \
        object2.position[1] + object2NegativeBuffer <= object1.position[1] + object1.height - object1NegativeBuffer <= object2.position[1] + object2.height - object2NegativeBuffer or \
        object2.position[0] + object2NegativeBuffer <= object1.position[0] + object1NegativeBuffer <= object2.position[0] + object2.width - object2NegativeBuffer and \
        object2.position[1] + object2NegativeBuffer <= object1.position[1] + object1.height - object1NegativeBuffer <= object2.position[1] + object2.height):
        return True

    else:
        return False
