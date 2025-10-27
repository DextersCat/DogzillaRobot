# Amy PiCrawler Coordinate System Mapping

## Current Date: October 26, 2025

## Coordinate System Discovery

### Visual vs PiCrawler Coordinate Mapping
- **Position 1**: right_front (from camera perspective)
- **Position 2**: left_front (from camera perspective) - **CONFIRMED via wave test**  
- **Position 3**: left_rear (from camera perspective)
- **Position 4**: right_rear (from camera perspective)

### Current ASYMMETRIC Stand Coordinates
```python
current_coord: [
    [45, 45, -50],  # Position 1 (right_front) - Higher stance
    [45, 0, -50],   # Position 2 (left_front) - Lower stance  
    [45, 0, -50],   # Position 3 (left_rear) - Lower stance
    [45, 45, -50]   # Position 4 (right_rear) - Higher stance
]
```

### Target SYMMETRIC Stand Coordinates
```python
symmetric_stand_coords = [
    [45, 45, -50],  # Position 1 (right_front) - Reference
    [45, 45, -50],  # Position 2 (left_front) - FIXED to match right
    [45, 45, -50],  # Position 3 (left_rear) - FIXED to match right  
    [45, 45, -50]   # Position 4 (right_rear) - Reference
]
```

### Camera Look-Up Coordinates (From Symmetric Base)
```python
look_up_coords = [
    [45, 45, -30],  # Position 1: Raise front leg
    [45, 45, -30],  # Position 2: Raise front leg
    [45, 45, -50],  # Position 3: Keep rear leg stable
    [45, 45, -50]   # Position 4: Keep rear leg stable
]
```

## API Endpoints Status
- `/api/stand` - Stand gesture (asymmetric currently)
- `/api/wave` - Wave gesture (Position 2 movement confirmed)
- `/api/sensors` - Sensor monitoring (working)
- `/api/command` - Voice commands (working)

## Next Steps
1. Fix stand function to use symmetric coordinates
2. Implement camera look-up function
3. Test voice command integration
4. Prepare for iPad testing and Teddy meeting