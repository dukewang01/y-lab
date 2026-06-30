#!/usr/bin/env python3
"""
商城订单 → CRM入库脚本
关联到现有CRM客人数据，更新或新增记录
"""
import csv, json, sys, os
from collections import defaultdict
sys.stdout.reconfigure(encoding='utf-8')

CRM_DIR = r'C:\Users\Duke Wang\.openclaw\workspace\knowledge_center\fb_crm'
ORDER_FILE = r'C:\Users\Duke Wang\.openclaw\workspace\media\incoming\商城订单2026-05-04.txt'

# ==== Load existing CRM ====
guests_file = os.path.join(CRM_DIR, 'guests.json')
visits_file = os.path.join(CRM_DIR, 'visits.json')
prefs_file = os.path.join(CRM_DIR, 'preferences.json')

guests = json.load(open(guests_file, 'r', encoding='utf-8-sig')) if os.path.exists(guests_file) else []
visits = json.load(open(visits_file, 'r', encoding='utf-8-sig')) if os.path.exists(visits_file) else []
prefs = json.load(open(prefs_file, 'r', encoding='utf-8-sig')) if os.path.exists(prefs_file) else []

print(f'CRM现有数据: {len(guests)}位客人 / {len(visits)}条到店 / {len(prefs)}条偏好')

# ==== Parse orders ====
with open(ORDER_FILE, 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

print(f'订单文件: {len(rows)}条')

# Build guest lookup
existing_by_phone = {}
for g in guests:
    phone = g.get('phone', '').strip()
    if phone:
        existing_by_phone[phone] = g

existing_by_name = {}
for g in guests:
    name = g.get('name', '').strip()
    if name:
        existing_by_name[name] = g

# ==== Process orders ====
new_guests = 0
updated_guests = 0
new_visits = 0
visit_data = []

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
    
    # Find or create guest
    guest = None
    # Try by member_id first
    for g in guests:
        if g.get('id') == member_id or g.get('open_id') == member_id:
            guest = g
            break
    
    # Try by phone
    if not guest and phone in existing_by_phone:
        guest = existing_by_phone[phone]
    
    # Create new guest
    if not guest:
        name_clean = contact.split('(')[0].split('（')[0].strip()
        guest = {
            'id': member_id or 'SHOP_' + phone,
            'name': name_clean or '微信用户',
            'phone': phone,
            'source': '小程序商城订单',
            'notes': '商城客户',
        }
        guests.append(guest)
        new_guests += 1
        if phone:
            existing_by_phone[phone] = guest
    
    # Create visit record
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
    visit_data.append(visit)
    new_visits += 1

print(f'\n入库结果:')
print(f'  新增客人: {new_guests}')
print(f'  更新客人: {updated_guests}')
print(f'  新增到店/购买记录: {new_visits}')

# ==== Analyze purchase patterns ====
from collections import Counter
product_counts = Counter()
amount_by_guest = defaultdict(float)
for v in visit_data:
    product_counts[v['product']] += 1
    amount_by_guest[v['guest_id']] += v['amount']

# Top spenders
print(f'\n消费TOP10客人:')
top_spenders = sorted(amount_by_guest.items(), key=lambda x: -x[1])[:10]
for gid, amt in top_spenders:
    gname = ''
    for g in guests:
        if g.get('id') == gid:
            gname = g.get('name','')
            break
    print(f'  {gname}: ¥{amt:,.0f} ({sum(1 for v in visit_data if v["guest_id"]==gid)}笔)')

# ==== Write back ====
with open(guests_file, 'w', encoding='utf-8') as f:
    json.dump(guests, f, ensure_ascii=False, indent=2)

with open(visits_file, 'w', encoding='utf-8') as f:
    json.dump(visits + visit_data, f, ensure_ascii=False, indent=2)

print(f'\n✅ CRM入库完成!')
print(f'  最终: {len(guests)}位客人 / {len(visits)+new_visits}条记录')
