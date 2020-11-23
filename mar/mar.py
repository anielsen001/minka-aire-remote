# create a minka-aire remote class
import gpiozero
import time

def create_relay( relay_pin ):
    """ create a relay object from the gpiozero module """
    return gpiozero.OutputDevice( relay_pin,
                                  active_high = False,
                                  initial_value = False )


class MinkaAireRemote( object ):

    LIGHT_UP_GPIO_PIN = 18
    LIGHT_DOWN_GPIO_PIN = 19
    
    FAN_LOW_GPIO_PIN = 20
    FAN_MED_GPIO_PIN = 21
    FAN_HIGH_GPIO_PIN = 22
    FAN_OFF_GPIO_PIN = 23
    FAN_DIR_GPIO_PIN = 24

    UNIT_SELECT_GPIO_PIN = 25

    PUSH_BUTTON_TIME = 0.5 # seconds
    
    def __init__( self, *args, **kwargs):

        # create relay object for each button to toggle
        self.light_up_relay = create_relay( self.LIGHT_UP_GPIO_PIN )
        self.light_down_relay = create_relay( self.LIGHT_DOWN_GPIO_PIN )
        self.fan_low_relay = create_relay( self.FAN_LOW_GPIO_PIN )
        self.fan_med_relay = create_relay( self.FAN_MED_GPIO_PIN )
        self.fan_high_relay = create_relay( self.FAN_HIGH_GPIO_PIN )
        self.fan_off_relay = create_relay( self.FAN_OFF_GPIO_PIN )
        self.fan_direction_relay = create_relay( self.FAN_DIR_GPIO_PIN )
        self.unit_select_relay = create_relay( self.UNIT_SELECT_GPIO_PIN )

    def push_button( self, button_relay ):
        button_relay.toggle()
        time.sleep( self.PUSH_BUTTON_TIME )
        button_relay.toggle()

    def toggle_light( self ):
        """
        toggle the light switch, on units without a dimmer the 
        up/down light switches just toggle the light on and off
        """
        self.push_button( self.light_up_relay )

    def fan_off( self ):
        """
        turn off the fan
        """
        self.push_button( self.fan_off_relay )

    def fan_low( self ):
        """
        turn off the fan
        """
        self.push_button( self.fan_low_relay )

    def fan_med( self ):
        """
        turn off the fan
        """
        self.push_button( self.fan_med_relay )

    def fan_high( self ):
        """
        turn off the fan
        """
        self.push_button( self.fan_high_relay )

        
