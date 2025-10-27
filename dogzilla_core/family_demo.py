#!/usr/bin/env python3
"""
Amy's Family Demo Script
Special performance for Uncle Jamie, JB, and Cousin Barclay!
"""

import sys
import os
import time

# Add the current directory to Python path
sys.path.append('/home/spencer/amy_core')

from postwake_router import say, do_wave

def family_demo():
    """Special family demonstration sequence"""
    
    print("🎬 Starting Amy's Family Demo...")
    print("📹 Ready for recording!")
    time.sleep(2)
    
    # 1. Greet Uncle Jamie and JB
    print("\n👋 Greeting Uncle Jamie and JB...")
    say("Hi Uncle Jamie and JB!")
    time.sleep(1)
    
    # 2. Funny self-introduction
    print("\n🤖 Amy's funny introduction...")
    say("I'm Amy, Spencer's robot assistant! I'm like Alexa, but with arms, legs, and a much better sense of humor!")
    time.sleep(1)
    
    # 3. Tell a joke
    print("\n😄 Telling a joke...")
    say("Here's a robot joke for you: Why don't robots ever panic? Because they have nerves of steel and backup batteries!")
    time.sleep(1)
    
    # 4. Greet Cousin Barclay
    print("\n🐻 Greeting Cousin Barclay...")
    say("And say hi to Cousin Barclay! I hear you're Teddy's cousin - the family resemblance is unbearable!")
    time.sleep(1)
    
    # 5. Wave goodbye
    print("\n👋 Waving goodbye...")
    say("Now let me give you all a proper robot wave goodbye!")
    do_wave()
    time.sleep(2)
    
    # 6. Weekend wishes
    print("\n🌟 Weekend wishes...")
    say("Have a fantastic weekend everyone! Remember, life's too short for boring robots!")
    
    print("\n🎬 Demo complete! Perfect for video! 📹")
    print("✅ Amy's family performance finished!")

if __name__ == "__main__":
    try:
        family_demo()
    except KeyboardInterrupt:
        print("\n🛑 Demo stopped by user")
    except Exception as e:
        print(f"❌ Error during demo: {e}")