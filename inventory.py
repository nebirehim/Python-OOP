"""Inventory module"""

from database.validator import validate_integer


class Resource:
    """Base class for all resources"""

    def __init__(self, name, manufacturer, total, allocated):
        """

        Args:
            name (str): name of the resource
            manufacturer (str): manufacturer of the resource
            total (int): current total amount of resources
            allocated (int): current count of in-use resources

        Note:
             `allocated` cannot exceed the `total` amount of resources
        """
        self._name = name
        self._manufacturer = manufacturer

        validate_integer('total', total, min_value=0)
        self._total = total

        validate_integer('allocated', allocated, 0, total,
                         custom_max_message='Allocated inventory cannot exceed the total inventory'
                         )
        self._allocated = allocated

    @property
    def name(self):
        """

        Returns:
            str: name of the resource
        """
        return self._name

    @property
    def manufacturer(self):
        """

        Returns:
            str: manufacturer of the resource

        """
        return self._manufacturer

    @property
    def total(self):
        """

        Returns:
            int: total amount of resources

        """
        return self._total

    @property
    def allocated(self):
        """

        Returns:
            int: count of in-use resources

        """
        return self._allocated

    @property
    def category(self):
        """


        Returns:
            str: category of the resource

        """
        return type(self).__name__.lower()

    @property
    def available(self):
        """


        Returns:
            int: count of available resources for use

        """
        return self.total - self.allocated

    def __str__(self):
        return self.name

    def __repr__(self):
        return (f'{self.name} ({self.category} - {self.manufacturer}): '
                f'total={self.total}, allocated={self.allocated}'
                )

    def claim(self, num):
        """
        Claim num inventory items (if available)
        Args:
            num (int): number of items to claim

        Returns:

        """
        validate_integer('num', num, 1, self.available,
                         custom_max_message='Cannot calim more than available items')

        self._allocated += num

    def freeup(self, num):
        """
        Return an inventory item to the available pool
        Args:
            num (int): number of items to return (cannot exceed number in-use resources)

        Returns:

        """
        validate_integer('num', num, 1, self.allocated,
                         custom_max_message='Cannot return more than allocated items'
                         )
        self._allocated -= num

    def died(self, num):
        """
        Number of items to deallocated and remove from the inventory pool
        Args:
            num (int): number of items that have died :

        Returns:

        """
        validate_integer('num', num, 1, self.allocated,
                         custom_max_message='Cannot retire more than allocated items')

        self._total -= num
        self._allocated -= num

    def purchased(self, num):
        """
        Add new inventory item to the pool
        Args:
            num (int): number of items to add to the pool:

        Returns:

        """
        validate_integer('num', num, 1)
        self._total += num


class CPU(Resource):
    """Resource subclass used to track specific CPU inventory pools"""

    def __init__(self, name, manufacturer, total, allocated,
                 cores, socket, power_watts):
        """

        Args:
            name (str): name of the resource
            manufacturer (str): manufacturer of the resource
            total (int) : total amount of resource
            allocated (int) : amount of in-use resources
            cores (int): number of cores
            socket (str): CPU socket type
            power_watts (int): CPU rated wattage
        """
        super().__init__(name, manufacturer, total, allocated)
        validate_integer('cores', cores, 1)
        validate_integer('power_watts', power_watts, 1)

        self._cores = cores
        self._socket = socket
        self._power_watts = power_watts

    @property
    def cores(self):
        """
        Number of cores
        Returns:
            int
        """
        return self._cores

    @property
    def socket(self):
        """
        CPU socket
        Returns:
            str
        """
        return self._socket

    @property
    def power_watts(self):
        """
        CPU power watts
        Returns:
            int
        """
        return self._power_watts

    def __repr__(self):
        return f'{self.category}: {self.name} ({self.socket} - x{self.cores})'


class Storage(Resource):
    """ A base class for storage devices"""

    def __init__(self, name, manufacturer, total, allocated, capacity_gb):
        """

        Args:
            name (str): name of the resource
            manufacturer (str): manufacturer of the resource
            total (int): total amount of resource
            allocated (int): amount of in-use resources
            capacity_gb (int): capacity of the storage device
        """
        super().__init__(name, manufacturer, total, allocated)
        validate_integer('capacity_gb', capacity_gb, 1)
        self._capacity_gb = capacity_gb

    @property
    def capacity_gb(self):
        """
        Capacity of the storage device
        Returns:
            int
        """
        return self._capacity_gb

    def __repr__(self):
        return f'{self.category}: {self._capacity_gb} GB'