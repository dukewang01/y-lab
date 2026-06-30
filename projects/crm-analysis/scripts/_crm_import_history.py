#!/usr/bin/env python3
"""
追加历史商城订单 → CRM入库
"""
import csv, json, sys, os
from collections import defaultdict
sys.stdout.reconfigure(encoding='utf-8')

CRM_DIR = r'C:\Users\Duke Wang\.openclaw\workspace\knowledge_center\fb_crm'
ORDER_FILE = r'C:\Users\Duke Wang\.openclaw\workspace\media\incoming\商城订单2026-05-04_历史.txt'

guests = json.load(open(os.path.join(CRM_DIR, 'guests.json'), 'r', encoding='utf-8-sig'))
visits = json.load(open(os.path.join(CRM_DIR, 'visits.json'), 'r', encoding='utf-8-sig'))
prefs = json.load(open(os.path.join(CRM_DIR, 'preferences.json'), 'r', encoding='utf-8-sig'))

print('CRM当前: ' + str(len(guests)) + '位客人 / ' + str(len(visits)) + '条到店')

with open(ORDER_FILE, 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

print('历史订单: ' + str(len(rows)) + '条')

# Build phone-to-guest lookup
by_phone = {}
by_id = {}
for g in guests:
    phone = g.get('phone', '').strip()
    gid = g.get('id', '')
    if phone:
        by_phone[phone] = g
    if gid:
        by_id[gid] = g

new_guests = 0
new_visits = 0
duplicate_visits = 0

for r in rows:
    contact = r.get('联系人', '').strip()
    phone = r.get('手机号', '').strip()
    product = r.get('商品名称', '').strip()
    amount = float(r.get('实付金额', 0) or 0)
    order_date = r.get('下单时间', '')[:10]
    status = r.get('商品状态', '')
    member_id = r.get('会员ID', '').strip()
    spec = r.get('规格名称', '').strip()
    staff_referrer = r.get('应获奖励人', '').strip()
    
    if not phone and not contact:
        continue
    
    # Find guest
    guest = by_id.get(member_id) or by_phone.get(phone)
    
    if not guest:
        name_clean = contact.split('(')[0].split('（')[0].strip()
        guest = {
            'id': member_id or 'SHOP_OLD_' + phone,
            'name': name_clean or '微信用户',
            'phone': phone,
            'source': '小程序商城订单(历史)',
            'notes': '商城客户(2025Q4-2026Q1)',
        }
        guests.append(guest)
        new_guests += 1
        if phone:
            by_phone[phone] = guest
        if member_id:
            by_id[member_id] = guest
    
    # Check duplicate (same guest, same product, same date)
    is_dup = False
    for v in visits:
        if (v.get('guest_id') == guest['id'] and 
            v.get('product') == product and 
            v.get('date') == order_date and
            v.get('type') == 'online_purchase'):
            is_dup = True
            duplicate_visits += 1
            break
    
    if not is_dup:
        visit = {
            'guest_id': guest['id'],
            'guest_name': guest['name'],
            'date': order_date,
            'type': 'online_purchase',
            'location': '小程序商城',
            'product': product,
            'spec': spec,
            'amount': amount,
            'status': status,
            'referrer': staff_referrer if staff_referrer and staff_referrer != '-' else '',
        }
        visits.append(visit)
        new_visits += 1

# Stats
total_rev = sum(float(r.get('实付金额',0) or 0) for r in rows)
used_rows = [r for r in rows if '已使用' in r.get('商品状态','')]
pending_rows = [r for r in rows if '待使用' in r.get('商品状态','')]
refunded_rows = [r for r in rows if '已退款' in r.get('商品状态','')]
used_rev = sum(float(r.get('实付金额',0) or 0) for r in used_rows)
pending_rev = sum(float(r.get('实付金额',0) or 0) for r in pending_rows)
refund_rev = sum(float(r.get('退实付',0) or 0) for r in refunded_rows)

dates = sorted(set(r.get('下单时间','')[:10] for r in rows if r.get('下单时间','')))
print(f'\n日期范围: {dates[0] if dates else "?"} ~ {dates[-1] if dates else "?"}')
print(f'总实付: ¥{total_rev:,.2f}')
print(f'已核销: ¥{used_rev:,.2f}')
print(f'待使用: ¥{pending_rev:,.2f}')
print(f'退款: {len(refunded_rows)}笔 ¥{refund_rev:,.2f}')
print(f'\n入库结果:')
print(f'  新增客人: {new_guests}')
print(f'  新增记录: {new_visits}')
print(f'  去重跳过: {duplicate_visits}')

# Write back
with open(os.path.join(CRM_DIR, 'guests.json'), 'w', encoding='utf-8') as f:
    json.dump(guests, f, ensure_ascii=False, indent=2)
with open(os.path.join(CRM_DIR, 'visits.json'), 'w', encoding='utf-8') as f:
    json.dump(visits, f, ensure_ascii=False, indent=2)

print(f'\n✅ CRM最终: {len(guests)}位客人 / {len(visits)}条记录')
