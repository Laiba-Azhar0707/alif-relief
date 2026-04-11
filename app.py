from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3, os

app = Flask(__name__)
app.secret_key = 'alif-relief-secret-2026'

DB_PATH = os.path.join('/data', 'alif_relief.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.executescript('''
        CREATE TABLE IF NOT EXISTS donors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, cnic TEXT, email TEXT,
            phone TEXT NOT NULL, city TEXT,
            type TEXT DEFAULT 'Individual',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS campaigns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, category TEXT,
            target REAL NOT NULL, status TEXT DEFAULT 'Active',
            start_date TEXT, end_date TEXT, description TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS donations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            donor_id INTEGER REFERENCES donors(id) ON DELETE SET NULL,
            campaign_id INTEGER REFERENCES campaigns(id) ON DELETE SET NULL,
            amount REAL NOT NULL, date TEXT NOT NULL,
            method TEXT DEFAULT 'Cash', status TEXT DEFAULT 'Received',
            notes TEXT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS beneficiaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, cnic TEXT, phone TEXT, city TEXT,
            category TEXT, members INTEGER DEFAULT 1,
            status TEXT DEFAULT 'Active',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS volunteers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, email TEXT, phone TEXT NOT NULL,
            city TEXT, skills TEXT, status TEXT DEFAULT 'Active',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def dashboard():
    conn = get_db()
    donors = conn.execute('SELECT COUNT(*) FROM donors').fetchone()[0]
    campaigns = conn.execute('SELECT COUNT(*) FROM campaigns').fetchone()[0]
    total = conn.execute('SELECT COALESCE(SUM(amount),0) FROM donations').fetchone()[0]
    beneficiaries = conn.execute('SELECT COUNT(*) FROM beneficiaries').fetchone()[0]
    recent_donations = conn.execute('''SELECT donations.*, donors.name as donor_name, campaigns.name as campaign_name
        FROM donations LEFT JOIN donors ON donations.donor_id=donors.id
        LEFT JOIN campaigns ON donations.campaign_id=campaigns.id
        ORDER BY donations.created_at DESC LIMIT 5''').fetchall()
    active_campaigns = conn.execute(
        "SELECT * FROM campaigns WHERE status='Active' ORDER BY created_at DESC LIMIT 5").fetchall()
    conn.close()
    return render_template('dashboard.html', donors=donors, campaigns=campaigns,
        total_donations=total, beneficiaries=beneficiaries,
        recent_donations=recent_donations, active_campaigns=active_campaigns)

@app.route('/donors')
def donors():
    conn = get_db()
    rows = conn.execute('SELECT * FROM donors ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('donors.html', donors=rows)

@app.route('/donors/add', methods=['POST'])
def add_donor():
    conn = get_db()
    conn.execute('INSERT INTO donors (name,cnic,email,phone,city,type) VALUES (?,?,?,?,?,?)',
        (request.form['name'], request.form.get('cnic'), request.form.get('email'),
         request.form['phone'], request.form.get('city'), request.form.get('type','Individual')))
    conn.commit(); conn.close()
    flash('Donor added successfully!', 'success')
    return redirect(url_for('donors'))

@app.route('/donors/delete/<int:did>', methods=['POST'])
def delete_donor(did):
    conn = get_db()
    conn.execute('DELETE FROM donors WHERE id=?', (did,))
    conn.commit(); conn.close()
    flash('Donor deleted.', 'info')
    return redirect(url_for('donors'))

@app.route('/campaigns')
def campaigns():
    conn = get_db()
    rows = conn.execute('SELECT * FROM campaigns ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('campaigns.html', campaigns=rows)

@app.route('/campaigns/add', methods=['POST'])
def add_campaign():
    conn = get_db()
    conn.execute('INSERT INTO campaigns (name,category,target,status,start_date,end_date,description) VALUES (?,?,?,?,?,?,?)',
        (request.form['name'], request.form.get('category'), request.form['target'],
         request.form.get('status','Active'), request.form.get('start_date'),
         request.form.get('end_date'), request.form.get('description')))
    conn.commit(); conn.close()
    flash('Campaign added!', 'success')
    return redirect(url_for('campaigns'))

@app.route('/campaigns/delete/<int:cid>', methods=['POST'])
def delete_campaign(cid):
    conn = get_db()
    conn.execute('DELETE FROM campaigns WHERE id=?', (cid,))
    conn.commit(); conn.close()
    flash('Campaign deleted.', 'info')
    return redirect(url_for('campaigns'))

@app.route('/donations')
def donations():
    conn = get_db()
    rows = conn.execute('''SELECT donations.*, donors.name as donor_name, campaigns.name as campaign_name
        FROM donations LEFT JOIN donors ON donations.donor_id=donors.id
        LEFT JOIN campaigns ON donations.campaign_id=campaigns.id
        ORDER BY donations.created_at DESC''').fetchall()
    donors_list = conn.execute('SELECT * FROM donors').fetchall()
    campaigns_list = conn.execute('SELECT * FROM campaigns').fetchall()
    conn.close()
    return render_template('donations.html', donations=rows, donors=donors_list, campaigns=campaigns_list)

@app.route('/donations/add', methods=['POST'])
def add_donation():
    conn = get_db()
    conn.execute('INSERT INTO donations (donor_id,campaign_id,amount,date,method,notes) VALUES (?,?,?,?,?,?)',
        (request.form.get('donor_id') or None, request.form.get('campaign_id') or None,
         request.form['amount'], request.form['date'],
         request.form.get('method','Cash'), request.form.get('notes')))
    conn.commit(); conn.close()
    flash('Donation recorded!', 'success')
    return redirect(url_for('donations'))

@app.route('/donations/delete/<int:did>', methods=['POST'])
def delete_donation(did):
    conn = get_db()
    conn.execute('DELETE FROM donations WHERE id=?', (did,))
    conn.commit(); conn.close()
    flash('Donation deleted.', 'info')
    return redirect(url_for('donations'))

@app.route('/beneficiaries')
def beneficiaries():
    conn = get_db()
    rows = conn.execute('SELECT * FROM beneficiaries ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('beneficiaries.html', beneficiaries=rows)

@app.route('/beneficiaries/add', methods=['POST'])
def add_beneficiary():
    conn = get_db()
    conn.execute('INSERT INTO beneficiaries (name,cnic,phone,city,category,members) VALUES (?,?,?,?,?,?)',
        (request.form['name'], request.form.get('cnic'), request.form.get('phone'),
         request.form.get('city'), request.form.get('category'), request.form.get('members',1)))
    conn.commit(); conn.close()
    flash('Beneficiary added!', 'success')
    return redirect(url_for('beneficiaries'))

@app.route('/beneficiaries/delete/<int:bid>', methods=['POST'])
def delete_beneficiary(bid):
    conn = get_db()
    conn.execute('DELETE FROM beneficiaries WHERE id=?', (bid,))
    conn.commit(); conn.close()
    flash('Beneficiary deleted.', 'info')
    return redirect(url_for('beneficiaries'))

@app.route('/volunteers')
def volunteers():
    conn = get_db()
    rows = conn.execute('SELECT * FROM volunteers ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('volunteers.html', volunteers=rows)

@app.route('/volunteers/add', methods=['POST'])
def add_volunteer():
    conn = get_db()
    conn.execute('INSERT INTO volunteers (name,email,phone,city,skills) VALUES (?,?,?,?,?)',
        (request.form['name'], request.form.get('email'), request.form['phone'],
         request.form.get('city'), request.form.get('skills')))
    conn.commit(); conn.close()
    flash('Volunteer added!', 'success')
    return redirect(url_for('volunteers'))

@app.route('/volunteers/delete/<int:vid>', methods=['POST'])
def delete_volunteer(vid):
    conn = get_db()
    conn.execute('DELETE FROM volunteers WHERE id=?', (vid,))
    conn.commit(); conn.close()
    flash('Volunteer deleted.', 'info')
    return redirect(url_for('volunteers'))

@app.route('/reports')
def reports():
    conn = get_db()
    total_raised = conn.execute('SELECT COALESCE(SUM(amount),0) FROM donations').fetchone()[0]
    total_donors = conn.execute('SELECT COUNT(*) FROM donors').fetchone()[0]
    total_beneficiaries = conn.execute('SELECT COUNT(*) FROM beneficiaries').fetchone()[0]
    total_volunteers = conn.execute('SELECT COUNT(*) FROM volunteers').fetchone()[0]
    campaign_stats = conn.execute('''SELECT campaigns.name, COALESCE(SUM(donations.amount),0) as raised, campaigns.target
        FROM campaigns LEFT JOIN donations ON campaigns.id=donations.campaign_id
        GROUP BY campaigns.id''').fetchall()
    conn.close()
    return render_template('reports.html', total_raised=total_raised, total_donors=total_donors,
        total_beneficiaries=total_beneficiaries, total_volunteers=total_volunteers,
        campaign_stats=campaign_stats)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=False)
