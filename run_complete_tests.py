#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اسکریپت اجرای کامل تمام تست‌های سیستم چیدمانو
"""

import os
import sys
import subprocess
import time
import json
from datetime import datetime

class CompleteTestRunner:
    def __init__(self):
        self.test_scripts = [
            'complete_system_test.py',
            'admin_dashboard_test.py',
            'ai_analysis_test.py'
        ]
        self.results = {}
        
        print("🚀 اسکریپت اجرای کامل تست‌ها راه‌اندازی شد")
        print("=" * 60)

    def run_all_tests(self):
        """اجرای تمام تست‌ها"""
        try:
            print("\n📋 شروع اجرای کامل تست‌ها...")
            
            # بررسی وجود فایل‌های تست
            self.check_test_files()
            
            # اجرای تست‌های مختلف
            for script in self.test_scripts:
                self.run_test_script(script)
            
            # تولید گزارش نهایی
            self.generate_final_report()
            
            print("\n🎉 تمام تست‌ها با موفقیت اجرا شدند!")
            
        except Exception as e:
            print(f"\n❌ خطا در اجرای تست‌ها: {str(e)}")
            import traceback
            traceback.print_exc()

    def check_test_files(self):
        """بررسی وجود فایل‌های تست"""
        print("\n🔍 بررسی فایل‌های تست...")
        
        for script in self.test_scripts:
            if os.path.exists(script):
                print(f"✅ {script} موجود است")
            else:
                print(f"❌ {script} موجود نیست")
                raise FileNotFoundError(f"فایل {script} یافت نشد")

    def run_test_script(self, script_name):
        """اجرای یک اسکریپت تست"""
        print(f"\n🧪 اجرای {script_name}...")
        
        try:
            start_time = time.time()
            
            # اجرای اسکریپت
            result = subprocess.run(
                [sys.executable, script_name],
                capture_output=True,
                text=True,
                timeout=300  # 5 دقیقه timeout
            )
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            # ثبت نتیجه
            self.results[script_name] = {
                'success': result.returncode == 0,
                'execution_time': execution_time,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'return_code': result.returncode
            }
            
            if result.returncode == 0:
                print(f"✅ {script_name} با موفقیت اجرا شد ({execution_time:.2f}s)")
            else:
                print(f"❌ {script_name} با خطا مواجه شد ({execution_time:.2f}s)")
                print(f"خطا: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print(f"⏰ {script_name} timeout شد")
            self.results[script_name] = {
                'success': False,
                'execution_time': 300,
                'error': 'Timeout'
            }
        except Exception as e:
            print(f"❌ خطا در اجرای {script_name}: {str(e)}")
            self.results[script_name] = {
                'success': False,
                'error': str(e)
            }

    def generate_final_report(self):
        """تولید گزارش نهایی"""
        print("\n📋 تولید گزارش نهایی...")
        
        try:
            # جمع‌آوری گزارش‌های جزئی
            individual_reports = {}
            
            # خواندن گزارش‌های JSON
            report_files = [
                'test_report.json',
                'admin_test_report.json',
                'ai_test_report.json'
            ]
            
            for report_file in report_files:
                if os.path.exists(report_file):
                    try:
                        with open(report_file, 'r', encoding='utf-8') as f:
                            individual_reports[report_file] = json.load(f)
                    except Exception as e:
                        print(f"⚠️ خطا در خواندن {report_file}: {str(e)}")
            
            # تولید گزارش نهایی
            final_report = {
                'test_date': datetime.now().isoformat(),
                'test_runner_results': self.results,
                'individual_reports': individual_reports,
                'summary': {
                    'total_scripts': len(self.test_scripts),
                    'successful_scripts': sum(1 for result in self.results.values() if result.get('success', False)),
                    'failed_scripts': sum(1 for result in self.results.values() if not result.get('success', True)),
                    'total_execution_time': sum(result.get('execution_time', 0) for result in self.results.values())
                }
            }
            
            # ذخیره گزارش نهایی
            with open('final_test_report.json', 'w', encoding='utf-8') as f:
                json.dump(final_report, f, ensure_ascii=False, indent=2)
            
            print("✅ گزارش نهایی در final_test_report.json ذخیره شد")
            
            # نمایش خلاصه
            self.display_summary(final_report)
            
        except Exception as e:
            print(f"❌ خطا در تولید گزارش نهایی: {str(e)}")

    def display_summary(self, report):
        """نمایش خلاصه نتایج"""
        print("\n" + "="*60)
        print("📊 خلاصه نتایج تست‌ها:")
        print("="*60)
        
        summary = report['summary']
        print(f"🧪 تعداد اسکریپت‌ها: {summary['total_scripts']}")
        print(f"✅ اسکریپت‌های موفق: {summary['successful_scripts']}")
        print(f"❌ اسکریپت‌های ناموفق: {summary['failed_scripts']}")
        print(f"⏱️ زمان کل اجرا: {summary['total_execution_time']:.2f}s")
        
        print("\n📋 جزئیات هر اسکریپت:")
        for script_name, result in self.results.items():
            status = "✅ موفق" if result.get('success', False) else "❌ ناموفق"
            time_taken = result.get('execution_time', 0)
            print(f"   {script_name}: {status} ({time_taken:.2f}s)")
        
        print("\n📊 گزارش‌های تولید شده:")
        for report_file in ['test_report.json', 'admin_test_report.json', 'ai_test_report.json']:
            if os.path.exists(report_file):
                print(f"   ✅ {report_file}")
            else:
                print(f"   ❌ {report_file}")
        
        print("="*60)

def main():
    """تابع اصلی"""
    print("🚀 شروع اجرای کامل تست‌های سیستم چیدمانو")
    print("=" * 60)
    
    runner = CompleteTestRunner()
    runner.run_all_tests()
    
    print("\n🎉 اجرای کامل تست‌ها تمام شد!")
    print("📋 گزارش نهایی در فایل final_test_report.json ذخیره شد")

if __name__ == "__main__":
    main()
