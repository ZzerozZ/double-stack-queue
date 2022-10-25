from queue import LifoQueue

from error import LeftStackFullException, QueueEmptyException


class DoubleStackQueue:
    def __init__(self, max_size: int = -1, timeout: float = 60):
        """
        Queue from 2 stacks
        :param max_size: max size of queue, if max size is equal or lower than 0, queue size is infinity
        :param timeout: timeout
        """
        self.left_stack = LifoQueue(max_size - 1)
        self.right_stack = LifoQueue(max_size - 1)
        self.timeout = timeout
        self.state = 1

    def __block(self):
        self.state = 0

    def __unblock(self):
        self.state = 1

    def __ready(self):
        return self.state == 1

    def __move_items_to_right_stack(self):
        """
        Move all items from left stack to right stack.
        Right stack is always empty when call this function
        """
        while not self.left_stack.empty():
            self.right_stack.put(self.left_stack.get())

    def get_left_size(self):
        """
        :return: size of left stack
        """
        return self.left_stack.qsize()

    def get_right_size(self):
        """
        :return: size of right stack
        """
        return self.right_stack.qsize()

    def empty(self):
        """
        Check queue is empty or not
        :return: True if queue is empty, else False
        """
        return self.left_stack.empty() and self.right_stack.empty()

    def full(self):
        """
        Check queue is full or not
        :return: True if no more item can be added
        """
        return self.left_stack.full() and (not self.right_stack.empty())

    def __put(self, item: object):
        """
        Add an item to queue
        :param item: any python object
        """
        # If left stack is not full, put item into it
        if not self.left_stack.full():
            self.left_stack.put(item, timeout=self.timeout)
        # If left stack is full, check right stack is empty or not
        else:
            if self.right_stack.empty():
                # If right stack is empty, move all items from left to right
                self.__move_items_to_right_stack()
                # Put item to left stack
                self.left_stack.put(item, timeout=self.timeout)
            else:
                # If left stack is full and right stack is not empty, no more item can be added
                raise LeftStackFullException("Queue is full, let's pop some items out")

    def __pop(self):
        """
        Get an item out of queue
        :return: last item which added to queue
        """
        if self.right_stack.empty():
            if self.left_stack.empty():
                # Queue is empty
                raise QueueEmptyException("Queue is empty")
            else:
                # Right stack is empty but left stack have some items. We need to move them to right stack to pop out
                self.__move_items_to_right_stack()
                return self.right_stack.get(timeout=self.timeout)
        else:
            return self.right_stack.get(timeout=self.timeout)

    def put(self, item: object):
        """
        Add an item to queue
        :param item: any python object
        """
        self.__block()
        try:
            self.__put(item)
        except Exception as e:
            print(f"ERROR: {e}")
        self.__unblock()

    def pop(self):
        """
        Get an item out of queue
        :return: last item which added to queue or None when failed
        """
        self.__block()
        try:
            return self.__pop()
        except Exception as e:
            print(f"ERROR: {e}")
        self.__unblock()

        return None
