#!/usr/bin/env python3
"""追加2022年11-12月历史商城订单 → CRM"""
import csv, json, sys, os
sys.stdout.reconfigure(encoding='utf-8')

CRM_DIR = r'C:\Users\Duke Wang\.openclaw\workspace\knowledge_center\fb_crm'
ORDER_FILE = r'C:\Users\Duke Wang\.openclaw\workspace\media\incoming\商城订单2026-05-04_2022NovDec.txt'

guests = json.load(open(os.path.join(CRM_DIR, 'guests.json'), 'r', encoding='utf-8-sig'))
visits = json.load(open(os.path.join(CRM_DIR, 'visits.json'), 'r', encoding='utf-8-sig'))

print('CRM当前: ' + str(len(guests)) + '位客人 / ' + str(len(visits)) + '条到店')

with open(ORDER_FILE, 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

print('历史订单(2022.11-12): ' + str(len(rows)) + '条')

by_phone = {}
by_id = {}
for g in guests:
    phone = g.get('phone', '').strip()
    gid = g.get('id', '')
    if phone: by_phone[phone] = g
    if gid: by_id[gid] = g

new_guests = 0
new_visits = 0
dup = 0

existing_triple = set()
for v in visits:
    if v.get('type') == 'online_purchase':
        existing_triple.add((v.get('guest_id',''), v.get('product',''), v.get('date','')))

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
    
    guest = by_id.get(member_id) or by_phone.get(phone)
    
    if not guest:
        name_clean = contact.split('(')[0].split('（')[0].strip()
        guest = {
            'id': member_id or 'SHOP_2022ND_' + phone,
            'name': name_clean or '微信用户',
            'phone': phone,
            'source': '小程序商城订单(2022.11-12)',
            'notes': '商城客户(2022.11-12)',
        }
        guests.append(guest)
        new_guests += 1
        if phone: by_phone[phone] = guest
        if member_id: by_id[member_id] = guest
    
    key = (guest['id'], product, order_date)
    if key in existing_triple:
        dup += 1
        continue
    
    existing_triple.add(key)
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

total_rev = sum(float(r.get('实付金额',0) or 0) for r in rows)
dates = sorted(set(r.get('下单时间','')[:10] for r in rows if r.get('下单时间','')))
print()
print('日期: ' + str(dates[0]) + ' ~ ' + str(dates[-1]))
print('总实付: ' + str(round(total_rev, 2)))
print('入库: 新客人' + str(new_guests) + ' / 新记录' + str(new_visits) + ' / 去重' + str(dup))

with open(os.path.join(CRM_DIR, 'guests.json'), 'w', encoding='utf-8') as f:
    json.dump(guests, f, ensure_ascii=False, indent=2)
with open(os.path.join(CRM_DIR, 'visits.json'), 'w', encoding='utf-8') as f:
    json.dump(visits, f, ensure_ascii=False, indent=2)

print('CRM最终: ' + str(len(guests)) + '位客人 / ' + str(len(visits)) + '条记录')
