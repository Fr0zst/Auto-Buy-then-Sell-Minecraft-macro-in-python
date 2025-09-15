# © 2025 Fr0zst. All rights reserved. 
# Unauthorized copying prohibited.

import pyautogui
import keyboard
import time
import random
from datetime import datetime

# Global variables
time_history = []
running = False
click_coordinates = {
    'bamboo': None,
    'chest': None, 
    'cyan': None,
    'diamond': None
}

# Disable pyautogui failsafe and set faster speed
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.05  # Reduced pause for faster execution

def show_banner():
    """Print a banner"""
    print("\033[92m" + "="*60)
    print("         MINECRAFT BAMBOO MONEY MAKER by Fr0zst")
    print("         Manual Coordinate System")
    print("="*60 + "\033[0m")

def random_delay(min_time=1.0, max_time=1.5):
    """Random delay between actions - now faster"""
    delay = random.uniform(min_time, max_time)
    time.sleep(delay)

def exact_delay(seconds):
    """Exact delay for precise timing"""
    time.sleep(seconds)

def get_mouse_position():
    """Get current mouse position"""
    x, y = pyautogui.position()
    return (x, y)

def safe_click(x, y, description=""):
    """Perform a safe click with proper positioning and confirmation"""
    try:
        # Move to position first
        pyautogui.moveTo(x, y, duration=0.2)
        time.sleep(0.2)  # Ensure movement completes
        
        # Double-click for important buttons like purchase
        if 'Diamond' in description or 'purchase' in description.lower():
            print(f"  💎 PURCHASE CLICK: Double-clicking {description}")
            pyautogui.click(x, y)
            time.sleep(0.3)
            pyautogui.click(x, y)  # Second click for purchase confirmation
            time.sleep(0.2)
        else:
            # Single click for other items
            pyautogui.click(x, y)
            time.sleep(0.2)  # Ensure click is registered
        
        if description:
            print(f"  ✅ Clicked {description} at ({x}, {y})")
        
        return True
    except Exception as e:
        print(f"  ❌ Failed to click {description}: {e}")
        return False

def setup_coordinates():
    """Manually set up click coordinates by positioning mouse"""
    global click_coordinates
    
    print("\n" + "="*60)
    print("🎯 COORDINATE SETUP")
    print("="*60)
    print("We'll capture the exact coordinates of each item.")
    print("\nSTEPS:")
    print("1. Open Minecraft")
    print("2. Type: /shop Farming")
    print("3. Position your mouse over each item when prompted")
    print("4. Press SPACE to save that position")
    print("\⚠️  IMPORTANT: Position mouse EXACTLY over the CENTER of each item!")
    
    input("\nPress ENTER when /shop Farming is open...")
    
    items = [
        ('bamboo', '🌿 BAMBOO - The item you want to buy'),
        ('chest', '📦 CHEST/CRATE - Changes to buying mode'),
        ('cyan', '🔵 CYAN/BLUE item - Sets quantity (+33)'),
        ('diamond', '💎 DIAMOND - Purchase/Confirm button')
    ]
    
    print("\n" + "="*60)
    
    for key, description in items:
        print(f"\nSETUP: {description}")
        print("-" * 50)
        print("1. Move your mouse EXACTLY over this item")
        print("2. Make sure it's centered on the item")
        print("3. Press SPACE to capture coordinates")
        
        # Wait for spacebar
        while True:
            if keyboard.is_pressed('space'):
                break
            time.sleep(0.1)
        
        # Get coordinates
        x, y = get_mouse_position()
        click_coordinates[key] = (x, y)
        
        print(f"✅ {description}")
        print(f"   Coordinates saved: ({x}, {y})")
        
        time.sleep(1)  # Prevent double capture
    
    print(f"\n🎉 SETUP COMPLETE!")
    print("="*60)
    print("Saved coordinates:")
    for key, coords in click_coordinates.items():
        if coords:
            print(f"  {key}: {coords}")
    
    return True

def save_coordinates_to_file():
    """Save coordinates to a file for reuse"""
    try:
        with open('minecraft_coords.txt', 'w') as f:
            f.write("# Minecraft Bamboo Automation Coordinates\n")
            for key, coords in click_coordinates.items():
                if coords:
                    f.write(f"{key}={coords[0]},{coords[1]}\n")
        print("✅ Coordinates saved to minecraft_coords.txt")
    except Exception as e:
        print(f"❌ Error saving coordinates: {e}")

def load_coordinates_from_file():
    """Load coordinates from file"""
    global click_coordinates
    
    try:
        with open('minecraft_coords.txt', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    parts = line.split('=')
                    if len(parts) == 2:
                        key = parts[0]
                        coords = parts[1].split(',')
                        if len(coords) == 2:
                            click_coordinates[key] = (int(coords[0]), int(coords[1]))
        
        loaded = sum(1 for coords in click_coordinates.values() if coords)
        print(f"📋 Loaded {loaded}/4 coordinates from file")
        return loaded == 4
    except FileNotFoundError:
        print("📋 No saved coordinates file found")
        return False
    except Exception as e:
        print(f"❌ Error loading coordinates: {e}")
        return False

def test_coordinates():
    """Test the saved coordinates by clicking on each item"""
    if not all(click_coordinates.values()):
        print("❌ Not all coordinates are set! Please run setup first.")
        return False
    
    print("\n🧪 TESTING COORDINATES")
    print("="*50)
    print("Make sure /shop Farming is open in Minecraft")
    input("Press ENTER to start clicking test...")
    
    items = [
        ('bamboo', '🌿 Bamboo'),
        ('chest', '📦 Chest'),
        ('cyan', '🔵 Cyan item'),
        ('diamond', '💎 Diamond')
    ]
    
    for key, name in items:
        if key in click_coordinates and click_coordinates[key]:
            x, y = click_coordinates[key]
            print(f"Clicking {name} at ({x}, {y})...")
            
            # Use safe click
            safe_click(x, y, name)
            time.sleep(1.2)  # Faster test timing
    
    print("✅ Click test completed!")
    print("Did all clicks hit the correct items? If not, re-run setup.")
    return True

def perform_bamboo_cycle():
    """Perform one complete bamboo buying and selling cycle"""
    if not all(click_coordinates.values()):
        print("❌ Coordinates not set! Run setup first.")
        return False
    
    try:
        print("🚀 Starting bamboo cycle...")
        
        # Step 1: Open shop
        print("Step 1: Opening shop...")
        pyautogui.press('t')
        time.sleep(0.8)
        pyautogui.typewrite('/shop Farming', interval=0.02)
        pyautogui.press('enter')
        random_delay(2.5, 3.0)  # Wait for shop to load
        
        # Step 2: Click sequence with improved timing
        click_sequence = [
            ('bamboo', '🌿 Bamboo (select item)'),
            ('chest', '📦 Chest (buying mode)'),
            ('cyan', '🔵 Cyan (+33 quantity)'),
            ('diamond', '💎 Diamond (purchase)')
        ]
        
        print("Step 2: Executing purchase sequence...")
        for i, (key, description) in enumerate(click_sequence, 1):
            x, y = click_coordinates[key]
            print(f"  {i}/4: {description}")
            
            # Use safe click and wait for it to complete
            if not safe_click(x, y, description):
                print(f"❌ Failed to click {description}")
                return False
            
            # Special handling for the final click (diamond/purchase)
            if key == 'diamond':
                print("  🔥 Final purchase click - using extended delay...")
                random_delay(2.0, 2.5)  # Longer delay for purchase confirmation
            else:
                # Faster delay between clicks (1-1.5 seconds)
                random_delay(1.0, 1.5)
        
        # Step 3: Close shop
        print("Step 3: Closing shop...")
        pyautogui.press('esc')
        random_delay(1, 1.5)
        
        # Step 4: Sell bamboo
        print("Step 4: Selling bamboo...")
        pyautogui.press('t')
        time.sleep(0.8)
        pyautogui.typewrite('/sellall BAMBOO', interval=0.02)
        pyautogui.press('enter')
        random_delay(1.5, 2.0)
        
        print("✅ Cycle completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error during cycle: {e}")
        return False

def start_money_making():
    """Start the automated money making process"""
    global running, time_history
    
    if not all(click_coordinates.values()):
        print("❌ Coordinates not set up! Please run coordinate setup first.")
        return
    
    print("\n" + "="*60)
    show_banner()
    print("🎯 STARTING MONEY MAKING MODE")
    print("="*60)
    print("🔄 Flow: Shop → Buy → Sell → Repeat")
    print("🛑 Press 'Z' to stop anytime")
    print("⚠️  Make sure Minecraft is focused!")
    
    # Show coordinates being used
    print(f"\n📋 Using coordinates:")
    for key, coords in click_coordinates.items():
        print(f"  {key}: {coords}")
    
    print("\n⏰ Starting in 5 seconds...")
    for i in range(5, 0, -1):
        print(f"   {i}...")
        time.sleep(1)
    
    print("🚀 MONEY MAKING STARTED!")
    
    running = True
    cycle_count = 0
    successful_cycles = 0
    failed_cycles = 0
    start_time = datetime.now()
    
    while running:
        cycle_count += 1
        cycle_start_time = datetime.now()
        
        print(f"\n{'💰'*20}")
        print(f"CYCLE #{cycle_count} - {cycle_start_time.strftime('%H:%M:%S')}")
        if cycle_count > 1:
            success_rate = (successful_cycles / (cycle_count - 1)) * 100
            print(f"Success Rate: {success_rate:.1f}%")
        print(f"{'💰'*20}")
        
        # Check for stop key
        if keyboard.is_pressed('z'):
            print("🛑 Stop key pressed!")
            break
        
        # Perform cycle
        if perform_bamboo_cycle():
            successful_cycles += 1
            time_history.append(cycle_start_time.strftime('%Y-%m-%d %H:%M:%S'))
            print(f"✅ CYCLE #{cycle_count} SUCCESS!")
            failed_cycles = 0
        else:
            failed_cycles += 1
            print(f"❌ CYCLE #{cycle_count} FAILED!")
            
            if failed_cycles >= 3:
                print("🛑 Too many failures. Stopping for safety.")
                break
        
        # Wait between cycles - faster timing
        if running:
            print(f"⏳ Waiting exactly 1.5 seconds before next cycle...")
            exact_delay(1.5)  # Faster between cycles
            
            # Check for stop during the delay
            for _ in range(15):  # Check 15 times during 1.5 seconds (every 0.1s)
                if keyboard.is_pressed('z'):
                    running = False
                    print("🛑 Stop key pressed during delay!")
                    break
                time.sleep(0.1)
    
    # Final stats
    running = False
    end_time = datetime.now()
    duration = end_time - start_time
    
    print(f"\n{'='*60}")
    print("📊 SESSION COMPLETE!")
    print(f"{'='*60}")
    print(f"⏰ Duration: {duration}")
    print(f"🔄 Total cycles: {cycle_count}")
    print(f"✅ Successful: {successful_cycles}")
    print(f"❌ Failed: {failed_cycles}")
    if cycle_count > 0:
        print(f"📈 Success rate: {(successful_cycles/cycle_count)*100:.1f}%")
        print(f"💰 Bamboo sold: ~{successful_cycles * 64} items")
    print(f"{'='*60}")

def show_current_coordinates():
    """Display current coordinates"""
    print(f"\n📋 CURRENT COORDINATES:")
    print("="*40)
    
    if not any(click_coordinates.values()):
        print("❌ No coordinates set up yet!")
        return
    
    for key, coords in click_coordinates.items():
        status = "✅" if coords else "❌"
        coord_str = f"({coords[0]}, {coords[1]})" if coords else "Not set"
        print(f"{status} {key}: {coord_str}")

def show_statistics():
    """Show session statistics"""
    if not time_history:
        print("📊 No statistics available yet.")
        return
    
    print(f"\n📊 STATISTICS")
    print("="*40)
    print(f"🔄 Successful cycles: {len(time_history)}")
    print(f"💰 Bamboo sold: ~{len(time_history) * 64} items")
    print(f"💵 Estimated value: ~${len(time_history) * 64 * 2}")
    
    print(f"\n📋 RECENT HISTORY:")
    recent = time_history[-10:] if len(time_history) > 10 else time_history
    for i, timestamp in enumerate(recent, 1):
        cycle_num = len(time_history) - len(recent) + i
        print(f"Cycle {cycle_num}: {timestamp}")
    
    if len(time_history) > 10:
        print(f"... and {len(time_history) - 10} more")

def main_menu():
    """Main menu"""
    global running
    
    # Try to load saved coordinates
    load_coordinates_from_file()
    
    print("🎮 MINECRAFT BAMBOO MONEY MAKER 🎮")
    print("Simple & Reliable Coordinate System")
    
    while True:
        print(f"\n{'='*60}")
        print("🏠 MAIN MENU BY FR0ZST")
        print(f"{'='*60}")
        print("1️⃣  📍 Setup Coordinates (Required first time)")
        print("2️⃣  🧪 Test Coordinates") 
        print("3️⃣  🚀 START MONEY MAKING")
        print("4️⃣  📊 View Statistics")
        print("5️⃣  📋 Show Current Coordinates")
        print("6️⃣  💾 Save Coordinates")
        print("7️⃣  🛑 Stop Program") 
        print("8️⃣  ❌ Exit")
        
        # Show status
        coords_set = sum(1 for coords in click_coordinates.values() if coords)
        if coords_set == 4:
            status = "✅ Ready! All coordinates set"
        elif coords_set > 0:
            status = f"⚠️ Partial setup ({coords_set}/4 coordinates)"
        else:
            status = "❌ No coordinates set - Run setup first!"
        
        print(f"\n📋 Status: {status}")
        
        if running:
            print("🟢 RUNNING - Press Z in Minecraft to stop")
        
        choice = input(f"\nEnter choice (1-8): ").strip()
        
        if choice == '1':
            setup_coordinates()
            
        elif choice == '2':
            test_coordinates()
            
        elif choice == '3':
            if running:
                print("⚠️ Already running!")
            else:
                start_money_making()
            
        elif choice == '4':
            show_statistics()
            
        elif choice == '5':
            show_current_coordinates()
            
        elif choice == '6':
            save_coordinates_to_file()
            
        elif choice == '7':
            running = False
            print("🛑 Program stopped")
            
        elif choice == '8':
            running = False
            print("👋 Goodbye! Happy money making!")
            break
            
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main_menu()

