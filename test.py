import asyncio
import aiofiles
import aiofiles.os
import time
import json
import tempfile
import os
from pathlib import Path
import random
import csv
from typing import List, Dict

# Basic aiofiles operations
async def basic_aiofiles_demo():
    """Demonstrate basic async file operations"""
    print("=== BASIC AIOFILES OPERATIONS ===")
    
    # Create a temporary directory for our demos
    temp_dir = Path(tempfile.gettempdir()) / "aiofiles_demo"
    await aiofiles.os.makedirs(temp_dir, exist_ok=True)
    
    print(f"📁 Working directory: {temp_dir}")
    
    # Example 1: Writing to a file asynchronously
    print("\n1. Writing to file asynchronously")
    sample_file = temp_dir / "sample.txt"
    
    async with aiofiles.open(sample_file, 'w') as f:
        # Write multiple lines asynchronously
        await f.write("Hello from async file operations!\n")
        await f.write("This is line 2\n")
        await f.write("AsyncIO makes file I/O non-blocking\n")
        
        # Write a loop of data
        for i in range(5):
            await f.write(f"Line {i + 4}: Generated content {i}\n")
    
    print(f"✅ Written to {sample_file.name}")
    
    # Example 2: Reading from a file asynchronously
    print("\n2. Reading from file asynchronously")
    async with aiofiles.open(sample_file, 'r') as f:
        print("📖 File contents:")
        
        # Read line by line
        line_number = 1
        async for line in f:
            print(f"   {line_number:2d}: {line.strip()}")
            line_number += 1
    
    # Example 3: Reading entire file at once
    print("\n3. Reading entire file at once")
    async with aiofiles.open(sample_file, 'r') as f:
        content = await f.read()
        print(f"📄 File size: {len(content)} characters")
        print(f"📄 Line count: {len(content.splitlines())} lines")
    
    # Example 4: Appending to file
    print("\n4. Appending to file")
    async with aiofiles.open(sample_file, 'a') as f:
        await f.write("\n--- Appended content ---\n")
        await f.write("This was added later\n")
    
    print("✅ Content appended")
    
    # Example 5: File operations (async os operations)
    print("\n5. File system operations")
    
    # Check if file exists
    exists = await aiofiles.os.path.exists(sample_file)
    print(f"📋 File exists: {exists}")
    
    # Get file stats
    stat_info = await aiofiles.os.stat(sample_file)
    print(f"📋 File size: {stat_info.st_size} bytes")
    print(f"📋 Modified time: {time.ctime(stat_info.st_mtime)}")
    
    # List directory contents
    print(f"📋 Directory contents:")
    async for entry in aiofiles.os.scandir(temp_dir):
        print(f"   {entry.name} ({'dir' if entry.is_dir() else 'file'})")
    
    return temp_dir

# Concurrent file operations
async def concurrent_file_operations_demo(temp_dir):
    """Demonstrate concurrent file operations for improved performance"""
    print("\n=== CONCURRENT FILE OPERATIONS ===")
    
    async def create_sample_file(file_id, size_kb):
        """Create a sample file with specified size"""
        file_path = temp_dir / f"sample_{file_id}.txt"
        print(f"📝 Creating {file_path.name} ({size_kb}KB)...")
        
        start_time = time.time()
        
        async with aiofiles.open(file_path, 'w') as f:
            # Generate content to reach desired size
            content_per_line = f"This is sample content for file {file_id} " * 10
            lines_needed = (size_kb * 1024) // len(content_per_line + "\n")
            
            for i in range(lines_needed):
                await f.write(f"{content_per_line} - Line {i}\n")
        
        duration = time.time() - start_time
        actual_size = (await aiofiles.os.stat(file_path)).st_size
        print(f"✅ {file_path.name}: {actual_size} bytes in {duration:.2f}s")
        return file_path
    
    async def read_and_analyze_file(file_path):
        """Read and analyze a file's content"""
        print(f"📖 Analyzing {file_path.name}...")
        start_time = time.time()
        
        line_count = 0
        word_count = 0
        char_count = 0
        
        async with aiofiles.open(file_path, 'r') as f:
            async for line in f:
                line_count += 1
                word_count += len(line.split())
                char_count += len(line)
        
        duration = time.time() - start_time
        print(f"📊 {file_path.name}: {line_count} lines, {word_count} words, {char_count} chars ({duration:.2f}s)")
        
        return {
            'file': file_path.name,
            'lines': line_count,
            'words': word_count,
            'chars': char_count,
            'duration': duration
        }
    
    # Create multiple files concurrently
    print("🚀 Creating multiple files concurrently...")
    create_start_time = time.time()
    
    create_tasks = [
        create_sample_file(1, 50),   # 50KB file
        create_sample_file(2, 30),   # 30KB file
        create_sample_file(3, 70),   # 70KB file
        create_sample_file(4, 40),   # 40KB file
        create_sample_file(5, 60),   # 60KB file
    ]
    
    created_files = await asyncio.gather(*create_tasks)
    create_duration = time.time() - create_start_time
    
    print(f"⏱️  Created {len(created_files)} files in {create_duration:.2f} seconds")
    
    # Now read and analyze all files concurrently
    print("\n🚀 Analyzing all files concurrently...")
    analyze_start_time = time.time()
    
    analyze_tasks = [read_and_analyze_file(file_path) for file_path in created_files]
    analysis_results = await asyncio.gather(*analyze_tasks)
    
    analyze_duration = time.time() - analyze_start_time
    
    print(f"\n⏱️  Analyzed {len(created_files)} files in {analyze_duration:.2f} seconds")
    print("📋 Analysis Summary:")
    
    total_lines = sum(r['lines'] for r in analysis_results)
    total_words = sum(r['words'] for r in analysis_results)
    total_chars = sum(r['chars'] for r in analysis_results)
    
    print(f"   Total lines: {total_lines:,}")
    print(f"   Total words: {total_words:,}")
    print(f"   Total chars: {total_chars:,}")
    
    # Compare with sequential processing time estimate
    sequential_estimate = sum(r['duration'] for r in analysis_results)
    speedup = sequential_estimate / analyze_duration
    
    print(f"💡 Sequential processing would take ~{sequential_estimate:.2f}s")
    print(f"💡 Async processing took {analyze_duration:.2f}s ({speedup:.1f}x faster!)")
    
    return created_files

# JSON file processing
async def json_file_processing_demo(temp_dir):
    """Demonstrate async JSON file processing"""
    print("\n=== JSON FILE PROCESSING ===")
    
    async def create_json_file(filename, data):
        """Create a JSON file with given data"""
        file_path = temp_dir / filename
        print(f"💾 Creating {filename}...")
        
        async with aiofiles.open(file_path, 'w') as f:
            json_str = json.dumps(data, indent=2)
            await f.write(json_str)
        
        print(f"✅ {filename} created")
        return file_path
    
    async def read_json_file(file_path):
        """Read and parse JSON file"""
        print(f"📖 Reading {file_path.name}...")
        
        async with aiofiles.open(file_path, 'r') as f:
            content = await f.read()
            data = json.loads(content)
        
        print(f"✅ {file_path.name} loaded ({len(data)} items)")
        return data
    
    async def process_json_data(data, operation):
        """Process JSON data with different operations"""
        print(f"⚙️  Processing data with operation: {operation}")
        
        if operation == "users_by_age":
            # Group users by age ranges
            age_groups = {"18-25": 0, "26-35": 0, "36-50": 0, "50+": 0}
            for user in data:
                age = user.get('age', 0)
                if 18 <= age <= 25:
                    age_groups["18-25"] += 1
                elif 26 <= age <= 35:
                    age_groups["26-35"] += 1
                elif 36 <= age <= 50:
                    age_groups["36-50"] += 1
                else:
                    age_groups["50+"] += 1
            return age_groups
            
        elif operation == "city_distribution":
            # Count users by city
            cities = {}
            for user in data:
                city = user.get('city', 'Unknown')
                cities[city] = cities.get(city, 0) + 1
            return dict(sorted(cities.items(), key=lambda x: x[1], reverse=True))
            
        elif operation == "average_score":
            # Calculate average score
            scores = [user.get('score', 0) for user in data]
            return sum(scores) / len(scores) if scores else 0
            
        elif operation == "top_performers":
            # Find top 10 users by score
            sorted_users = sorted(data, key=lambda x: x.get('score', 0), reverse=True)
            return sorted_users[:10]
    
    # Generate sample data
    print("🎲 Generating sample JSON data...")
    
    cities = ["New York", "London", "Tokyo", "Sydney", "Paris", "Berlin", "Toronto", "Singapore"]
    departments = ["Engineering", "Sales", "Marketing", "HR", "Finance", "Operations"]
    
    datasets = {
        "users_dataset_1.json": [
            {
                "id": i,
                "name": f"User_{i:04d}",
                "age": random.randint(22, 65),
                "city": random.choice(cities),
                "department": random.choice(departments),
                "score": random.randint(60, 100),
                "active": random.choice([True, False])
            }
            for i in range(1000)  # 1000 users
        ],
        
        "users_dataset_2.json": [
            {
                "id": i + 1000,
                "name": f"User_{i + 1000:04d}",
                "age": random.randint(20, 60),
                "city": random.choice(cities),
                "department": random.choice(departments),
                "score": random.randint(50, 95),
                "active": random.choice([True, False])
            }
            for i in range(800)  # 800 users
        ],
        
        "users_dataset_3.json": [
            {
                "id": i + 1800,
                "name": f"User_{i + 1800:04d}",
                "age": random.randint(25, 55),
                "city": random.choice(cities),
                "department": random.choice(departments),
                "score": random.randint(70, 100),
                "active": random.choice([True, False])
            }
            for i in range(1200)  # 1200 users
        ]
    }
    
    # Create JSON files concurrently
    print("🚀 Creating JSON files concurrently...")
    create_tasks = [
        create_json_file(filename, data)
        for filename, data in datasets.items()
    ]
    
    json_files = await asyncio.gather(*create_tasks)
    
    # Read JSON files concurrently
    print("\n🚀 Reading JSON files concurrently...")
    read_tasks = [read_json_file(file_path) for file_path in json_files]
    json_data = await asyncio.gather(*read_tasks)
    
    # Process data with different operations concurrently
    print("\n🚀 Processing JSON data with multiple operations...")
    
    all_data = []
    for data_list in json_data:
        all_data.extend(data_list)
    
    print(f"📊 Combined dataset: {len(all_data)} users")
    
    processing_tasks = [
        process_json_data(all_data, "users_by_age"),
        process_json_data(all_data, "city_distribution"),
        process_json_data(all_data, "average_score"),
        process_json_data(all_data, "top_performers")
    ]
    
    results = await asyncio.gather(*processing_tasks)
    
    # Display results
    print("\n📋 Processing Results:")
    print(f"   Age Distribution: {results[0]}")
    print(f"   City Distribution (top 3): {dict(list(results[1].items())[:3])}")
    print(f"   Average Score: {results[2]:.2f}")
    print(f"   Top Performer: {results[3][0]['name']} (Score: {results[3][0]['score']})")

# CSV file processing
async def csv_file_processing_demo(temp_dir):
    """Demonstrate async CSV file processing"""
    print("\n=== CSV FILE PROCESSING ===")
    
    async def create_csv_file(filename, headers, data):
        """Create a CSV file with given headers and data"""
        file_path = temp_dir / filename
        print(f"📊 Creating {filename}...")
        
        async with aiofiles.open(file_path, 'w', newline='') as f:
            # Write headers
            header_line = ','.join(headers) + '\n'
            await f.write(header_line)
            
            # Write data rows
            for row in data:
                row_line = ','.join(str(row.get(header, '')) for header in headers) + '\n'
                await f.write(row_line)
        
        print(f"✅ {filename} created with {len(data)} rows")
        return file_path
    
    async def read_csv_file(file_path):
        """Read CSV file and return data"""
        print(f"📖 Reading {file_path.name}...")
        
        data = []
        async with aiofiles.open(file_path, 'r') as f:
            # Read header
            header_line = await f.readline()
            headers = [h.strip() for h in header_line.strip().split(',')]
            
            # Read data rows
            async for line in f:
                if line.strip():
                    values = [v.strip() for v in line.strip().split(',')]
                    row = dict(zip(headers, values))
                    data.append(row)
        
        print(f"✅ {file_path.name} loaded ({len(data)} rows)")
        return data, headers
    
    async def analyze_csv_data(data, filename, analysis_type):
        """Analyze CSV data"""
        print(f"📊 Analyzing {filename} - {analysis_type}")
        
        if analysis_type == "sales_summary":
            # Calculate sales statistics
            total_sales = sum(float(row.get('amount', 0)) for row in data)
            avg_sale = total_sales / len(data) if data else 0
            max_sale = max((float(row.get('amount', 0)) for row in data), default=0)
            
            return {
                'file': filename,
                'total_sales': total_sales,
                'average_sale': avg_sale,
                'max_sale': max_sale,
                'transaction_count': len(data)
            }
            
        elif analysis_type == "product_performance":
            # Analyze product performance
            product_sales = {}
            for row in data:
                product = row.get('product', 'Unknown')
                amount = float(row.get('amount', 0))
                if product in product_sales:
                    product_sales[product]['total'] += amount
                    product_sales[product]['count'] += 1
                else:
                    product_sales[product] = {'total': amount, 'count': 1}
            
            # Calculate average per product
            for product in product_sales:
                product_sales[product]['average'] = (
                    product_sales[product]['total'] / product_sales[product]['count']
                )
            
            return {
                'file': filename,
                'products': product_sales
            }
    
    # Generate sample CSV data
    print("🎲 Generating sample CSV data...")
    
    products = ["Laptop", "Phone", "Tablet", "Headphones", "Mouse", "Keyboard", "Monitor", "Speaker"]
    regions = ["North", "South", "East", "West", "Central"]
    
    csv_datasets = {
        "sales_q1.csv": {
            "headers": ["date", "product", "region", "amount", "quantity"],
            "data": [
                {
                    "date": f"2024-{random.randint(1, 3):02d}-{random.randint(1, 28):02d}",
                    "product": random.choice(products),
                    "region": random.choice(regions),
                    "amount": round(random.uniform(50, 2000), 2),
                    "quantity": random.randint(1, 10)
                }
                for _ in range(500)  # 500 transactions
            ]
        },
        
        "sales_q2.csv": {
            "headers": ["date", "product", "region", "amount", "quantity"],
            "data": [
                {
                    "date": f"2024-{random.randint(4, 6):02d}-{random.randint(1, 28):02d}",
                    "product": random.choice(products),
                    "region": random.choice(regions),
                    "amount": round(random.uniform(50, 2000), 2),
                    "quantity": random.randint(1, 10)
                }
                for _ in range(450)  # 450 transactions
            ]
        },
        
        "sales_q3.csv": {
            "headers": ["date", "product", "region", "amount", "quantity"],
            "data": [
                {
                    "date": f"2024-{random.randint(7, 9):02d}-{random.randint(1, 28):02d}",
                    "product": random.choice(products),
                    "region": random.choice(regions),
                    "amount": round(random.uniform(50, 2000), 2),
                    "quantity": random.randint(1, 10)
                }
                for _ in range(600)  # 600 transactions
            ]
        }
    }
    
    # Create CSV files concurrently
    print("🚀 Creating CSV files concurrently...")
    create_tasks = [
        create_csv_file(filename, data["headers"], data["data"])
        for filename, data in csv_datasets.items()
    ]
    
    csv_files = await asyncio.gather(*create_tasks)
    
    # Read CSV files concurrently
    print("\n🚀 Reading CSV files concurrently...")
    read_tasks = [read_csv_file(file_path) for file_path in csv_files]
    csv_data_results = await asyncio.gather(*read_tasks)
    
    # Analyze data concurrently
    print("\n🚀 Analyzing CSV data concurrently...")
    analysis_tasks = []
    
    for (data, headers), file_path in zip(csv_data_results, csv_files):
        analysis_tasks.extend([
            analyze_csv_data(data, file_path.name, "sales_summary"),
            analyze_csv_data(data, file_path.name, "product_performance")
        ])
    
    analysis_results = await asyncio.gather(*analysis_tasks)
    
    # Display results
    print("\n📋 CSV Analysis Results:")
    for result in analysis_results:
        if 'total_sales' in result:
            print(f"   📊 {result['file']}: ${result['total_sales']:,.2f} total, "
                  f"${result['average_sale']:.2f} avg, {result['transaction_count']} transactions")
        elif 'products' in result:
            top_product = max(result['products'].items(), key=lambda x: x[1]['total'])
            print(f"   🏆 {result['file']}: Top product: {top_product[0]} "
                  f"(${top_product[1]['total']:,.2f} total)")

# Large file processing with streaming
async def large_file_processing_demo(temp_dir):
    """Demonstrate processing large files efficiently with streaming"""
    print("\n=== LARGE FILE PROCESSING ===")
    
    async def create_large_file(filename, size_mb):
        """Create a large file for testing"""
        file_path = temp_dir / filename
        print(f"📁 Creating large file {filename} (~{size_mb}MB)...")
        
        start_time = time.time()
        lines_written = 0
        
        async with aiofiles.open(file_path, 'w') as f:
            # Generate content to reach desired size
            sample_line = "This is a sample line with some content to make the file larger. " * 10 + "\n"
            line_size = len(sample_line)
            target_size = size_mb * 1024 * 1024
            lines_needed = target_size // line_size
            
            # Write in batches for better performance
            batch_size = 1000
            batch = []
            
            for i in range(lines_needed):
                batch.append(f"Line {i:06d}: {sample_line}")
                
                if len(batch) >= batch_size:
                    await f.write(''.join(batch))
                    batch = []
                    lines_written += batch_size
                    
                    # Show progress every 10,000 lines
                    if lines_written % 10000 == 0:
                        progress = (lines_written / lines_needed) * 100
                        print(f"   Progress: {progress:.1f}% ({lines_written:,} lines)")
            
            # Write remaining batch
            if batch:
                await f.write(''.join(batch))
                lines_written += len(batch)
        
        duration = time.time() - start_time
        actual_size = (await aiofiles.os.stat(file_path)).st_size / (1024 * 1024)
        
        print(f"✅ {filename}: {actual_size:.1f}MB, {lines_written:,} lines in {duration:.2f}s")
        return file_path
    
    async def process_large_file_streaming(file_path, operation):
        """Process large file using streaming (line by line)"""
        print(f"🔄 Processing {file_path.name} with {operation} (streaming)...")
        
        start_time = time.time()
        result = None
        
        if operation == "line_count":
            count = 0
            async with aiofiles.open(file_path, 'r') as f:
                async for line in f:
                    count += 1
                    
                    # Progress update every 50,000 lines
                    if count % 50000 == 0:
                        print(f"   Processed {count:,} lines...")
            
            result = f"Total lines: {count:,}"
            
        elif operation == "word_count":
            word_count = 0
            line_count = 0
            
            async with aiofiles.open(file_path, 'r') as f:
                async for line in f:
                    line_count += 1
                    word_count += len(line.split())
                    
                    # Progress update every 25,000 lines
                    if line_count % 25000 == 0:
                        print(f"   Processed {line_count:,} lines, {word_count:,} words...")
            
            result = f"Total words: {word_count:,} in {line_count:,} lines"
            
        elif operation == "pattern_search":
            matches = 0
            line_count = 0
            pattern = "sample line"
            
            async with aiofiles.open(file_path, 'r') as f:
                async for line in f:
                    line_count += 1
                    if pattern.lower() in line.lower():
                        matches += 1
                    
                    # Progress update every 30,000 lines
                    if line_count % 30000 == 0:
                        print(f"   Searched {line_count:,} lines, found {matches:,} matches...")
            
            result = f"Found '{pattern}' in {matches:,} lines out of {line_count:,}"
        
        duration = time.time() - start_time
        print(f"✅ {operation} completed in {duration:.2f}s: {result}")
        
        return {
            'operation': operation,
            'file': file_path.name,
            'result': result,
            'duration': duration
        }
    
    # Create a moderately large file (adjust size based on your system)
    large_file = await create_large_file("large_sample.txt", 5)  # 5MB file
    
    # Process the large file with different operations concurrently
    print("\n🚀 Processing large file with multiple operations concurrently...")
    
    processing_tasks = [
        process_large_file_streaming(large_file, "line_count"),
        process_large_file_streaming(large_file, "word_count"),
        process_large_file_streaming(large_file, "pattern_search")
    ]
    
    processing_results = await asyncio.gather(*processing_tasks)
    
    print("\n📋 Large File Processing Results:")
    total_processing_time = sum(r['duration'] for r in processing_results)
    max_processing_time = max(r['duration'] for r in processing_results)
    
    for result in processing_results:
        print(f"   {result['operation']}: {result['result']} ({result['duration']:.2f}s)")
    
    print(f"\n💡 Sequential processing would take ~{total_processing_time:.2f}s")
    print(f"💡 Concurrent processing took {max_processing_time:.2f}s")
    print(f"💡 Speedup: {total_processing_time / max_processing_time:.1f}x faster!")

# File monitoring and watching
async def file_monitoring_demo(temp_dir):
    """Demonstrate file monitoring and change detection"""
    print("\n=== FILE MONITORING ===")
    
    monitor_file = temp_dir / "monitored_file.txt"
    
    async def file_monitor(file_path, duration=10):
        """Monitor file changes for a specified duration"""
        print(f"👁️  Monitoring {file_path.name} for {duration} seconds...")
        
        # Initial file state
        try:
            initial_stat = await aiofiles.os.stat(file_path)
            last_modified = initial_stat.st_mtime
            last_size = initial_stat.st_size
            print(f"   Initial: {last_size} bytes, modified {time.ctime(last_modified)}")
        except FileNotFoundError:
            print(f"   File doesn't exist yet, waiting for creation...")
            last_modified = 0
            last_size = 0
        
        start_time = time.time()
        change_count = 0
        
        while time.time() - start_time < duration:
            try:
                current_stat = await aiofiles.os.stat(file_path)
                current_modified = current_stat.st_mtime
                current_size = current_stat.st_size
                
                # Check for changes
                if current_modified != last_modified or current_size != last_size:
                    change_count += 1
                    change_type = []
                    
                    if current_size != last_size:
                        if current_size > last_size:
                            change_type.append(f"size increased by {current_size - last_size} bytes")
                        else:
                            change_type.append(f"size decreased by {last_size - current_size} bytes")
                    
                    if current_modified != last_modified:
                        change_type.append("modification time changed")
                    
                    print(f"   📝 Change #{change_count}: {', '.join(change_type)}")
                    print(f"      New size: {current_size} bytes at {time.ctime(current_modified)}")
                    
                    last_modified = current_modified
                    last_size = current_size
                
            except FileNotFoundError:
                if last_size > 0:  # File was deleted
                    change_count += 1
                    print(f"   🗑️  Change #{change_count}: File was deleted")
                    last_modified = 0
                    last_size = 0
            
            # Check every 0.5 seconds
            await asyncio.sleep(0.5)
        
        print(f"   Monitoring completed: {change_count} changes detected")
        return change_count
    
    async def file_modifier(file_path, operations):
        """Modify file with various operations"""
        print(f"✏️  Starting file modifications on {file_path.name}...")
        
        await asyncio.sleep(1)  # Wait a bit before starting
        
        for i, (operation, delay) in enumerate(operations):
            print(f"   Operation {i+1}: {operation}")
            
            if operation == "create":
                async with aiofiles.open(file_path, 'w') as f:
                    await f.write("Initial content\n")
                    
            elif operation == "append":
                async with aiofiles.open(file_path, 'a') as f:
                    await f.write(f"Appended line at {time.strftime('%H:%M:%S')}\n")
                    
            elif operation == "overwrite":
                async with aiofiles.open(file_path, 'w') as f:
                    await f.write(f"File overwritten at {time.strftime('%H:%M:%S')}\n")
                    
            elif operation == "large_append":
                async with aiofiles.open(file_path, 'a') as f:
                    content = "Large content block: " + "x" * 1000 + "\n"
                    await f.write(content)
            
            await asyncio.sleep(delay)
        
        print("   File modifications completed")
    
    # Define modification operations
    modifications = [
        ("create", 1),        # Create file, wait 1s
        ("append", 1.5),      # Append text, wait 1.5s
        ("append", 1),        # Append more text, wait 1s
        ("large_append", 2),  # Append large content, wait 2s
        ("overwrite", 1.5),   # Overwrite file, wait 1.5s
        ("append", 1),        # Final append, wait 1s
    ]
    
    # Run monitor and modifier concurrently
    print("🚀 Starting file monitor and modifier concurrently...")
    
    monitor_task = asyncio.create_task(file_monitor(monitor_file, 12))
    modifier_task = asyncio.create_task(file_modifier(monitor_file, modifications))
    
    # Wait for both to complete
    changes_detected, _ = await asyncio.gather(monitor_task, modifier_task)
    
    print(f"📊 File monitoring completed: {changes_detected} changes detected")

# Cleanup and summary
async def cleanup_and_summary(temp_dir):
    """Clean up temporary files and provide summary"""
    print("\n=== CLEANUP & SUMMARY ===")
    
    print("🧹 Cleaning up temporary files...")
    
    file_count = 0
    total_size = 0
    
    # List all files before cleanup
    try:
        async for entry in aiofiles.os.scandir(temp_dir):
            if entry.is_file():
                file_count += 1
                stat_info = await aiofiles.os.stat(entry.path)
                total_size += stat_info.st_size
        
        print(f"📋 Found {file_count} files totaling {total_size / (1024*1024):.2f} MB")
        
        # Remove all files
        async for entry in aiofiles.os.scandir(temp_dir):
            if entry.is_file():
                await aiofiles.os.remove(entry.path)
        
        # Remove directory
        await aiofiles.os.rmdir(temp_dir)
        
        print("✅ Cleanup completed")
        
    except Exception as e:
        print(f"❌ Cleanup error: {e}")
    
    # Summary of what we learned
    print("\n🎓 AIOFILES TUTORIAL SUMMARY")
    print("=" * 50)
    print("✅ Basic async file operations (read, write, append)")
    print("✅ Concurrent file processing for better performance")
    print("✅ JSON file handling with async I/O")
    print("✅ CSV file processing and analysis")
    print("✅ Large file streaming for memory efficiency")
    print("✅ File monitoring and change detection")
    print("\n💡 Key Benefits of Async File I/O:")
    print("   • Non-blocking operations allow other tasks to run")
    print("   • Concurrent file processing improves overall performance")
    print("   • Memory-efficient streaming for large files")
    print("   • Real-time file monitoring capabilities")
    print("   • Better resource utilization in I/O-heavy applications")

# Main demonstration function
async def run_aiofiles_demos():
    """Run all aiofiles demonstrations"""
    print("📁 AsyncIO File Handling Tutorial")
    print("=" * 60)
    
    try:
        # Basic operations
        temp_dir = await basic_aiofiles_demo()
        
        # Concurrent file operations
        created_files = await concurrent_file_operations_demo(temp_dir)
        
        # JSON processing
        await json_file_processing_demo(temp_dir)
        
        # CSV processing
        await csv_file_processing_demo(temp_dir)
        
        # Large file processing
        await large_file_processing_demo(temp_dir)
        
        # File monitoring
        await file_monitoring_demo(temp_dir)
        
        # Cleanup
        await cleanup_and_summary(temp_dir)
        
        print("\n🎉 All aiofiles demos completed successfully!")
        
    except KeyboardInterrupt:
        print("\n🛑 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        import traceback
        traceback.print_exc()

# Run the demonstrations
if __name__ == "__main__":
    # Note: aiofiles needs to be installed first
    # pip install aiofiles
    
    print("📦 Make sure aiofiles is installed: pip install aiofiles")
    print("🚀 Starting aiofiles demonstrations...\n")
    
    try:
        asyncio.run(run_aiofiles_demos())
    except ImportError:
        print("❌ aiofiles library not found!")
        print("💡 Install it with: pip install aiofiles")
        print("💡 Then run this script again")
    except Exception as e:
        print(f"❌ Error running demos: {e}")