#include <bits/stdc++.h>
using namespace std;

double DMIN = -100;
double DMAX = 100;

struct evt {
    pair<double, double> beg, end;
    bool insert;
    int polygon;
};

void print_evt(evt e) {
    cout << "(" << e.beg.first << ", " << e.beg.second << "), (" << e.end.first << ", " << e.end.second << ")" << endl;
    cout << "insert = " << e.insert << endl;
    cout << "polygon = " << e.polygon << endl;
}

void print_events(map<double, vector<evt> >& events) {
    for (auto it = events.begin(); it != events.end(); it++) {
        cout << "xcoord = " << it->first << endl;
        for (int i = 0; i < (it->second).size(); i++) {
            print_evt((it->second)[i]);
        }
        cout << endl;
    }
}

bool esquerda(double X1, double Y1, double X2, double Y2, double X3, double Y3) {
    return ((X2 - X1) * (Y3 - Y1) - (X3 - X1) * (Y2 - Y1) >= 0);
}

struct hor_line {
    pair<double, double> beg, end;
    int polygon;
};

bool operator==(const hor_line& lhs, const hor_line& rhs) {
        return (lhs.beg.first == rhs.beg.first && lhs.beg.second == rhs.beg.second &&
                lhs.end.first == rhs.end.first && lhs.end.second == rhs.end.second && lhs.polygon == rhs.polygon);
    }

bool operator<(const hor_line& lhs, const hor_line& rhs) {
        bool b1, b2;
        b1 = esquerda(rhs.beg.first, rhs.beg.second, rhs.end.first, rhs.end.second, lhs.beg.first, lhs.beg.second);
        b2 = esquerda(rhs.beg.first, rhs.beg.second, rhs.end.first, rhs.end.second, lhs.end.first, lhs.end.second);
        if (b1 && b2) {
            return false;
        }
        if (!b1 && !b2) {
            return true;
        }
        b1 = esquerda(lhs.beg.first, lhs.beg.second, lhs.end.first, lhs.end.second, rhs.beg.first, rhs.beg.second);
        b2 = esquerda(lhs.beg.first, lhs.beg.second, lhs.end.first, lhs.end.second, rhs.end.first, rhs.end.second);
        if (b1 && b2) {
            return true;
        }
        return false;
    }

struct slab {
    double beg, end;
    vector<hor_line> lines;
};

void make_events(vector<vector<pair<double, double> > >& polygons, map<double, vector<evt> >& events) {
    pair<double, double> lp, rp;
    int poly;
    for (int i = 0; i < polygons.size(); i++) {
        for (int j = 0; j < polygons[i].size(); j++) {
            if (polygons[i][j].first < polygons[i][(j + 1) % polygons[i].size()].first) {
                lp.first = polygons[i][j].first;
                lp.second = polygons[i][j].second;
                rp.first = polygons[i][(j + 1) % polygons[i].size()].first;
                rp.second = polygons[i][(j + 1) % polygons[i].size()].second;
                poly = i;
            }
            else {
                rp.first = polygons[i][j].first;
                rp.second = polygons[i][j].second;
                lp.first = polygons[i][(j + 1) % polygons[i].size()].first;
                lp.second = polygons[i][(j + 1) % polygons[i].size()].second;
                poly = -1;
            }
            evt b, e;
            b.beg.first = e.beg.first = lp.first;
            b.beg.second = e.beg.second = lp.second;
            b.end.first = e.end.first = rp.first;
            b.end.second = e.end.second = rp.second;
            b.insert = true;
            e.insert = false;
            b.polygon = e.polygon = poly;
            events[lp.first].push_back(b);
            events[rp.first].push_back(e);
        }
    }
}

slab make_slab(slab base, const multiset<hor_line>& abb) {
    for (auto it = abb.begin(); it != abb.end(); it++) {
        base.lines.push_back(*it);
    }
    return base;
}

void update_abb(multiset<hor_line>& abb, evt e) {
    hor_line l;
    l.beg.first = e.beg.first;
    l.beg.second = e.beg.second;
    l.end.first = e.end.first;
    l.end.second = e.end.second;
    l.polygon = e.polygon;
    if (e.insert) {
        abb.insert(l);
    }
    else {
        abb.erase(l);
    }
}

void make_slabs(vector<slab>& s, map<double, vector<evt> >& events) {
    multiset<hor_line> abb;
    slab curr;
    hor_line cel;
    cel.beg.first = DMIN;
    cel.beg.second = DMAX;
    cel.end.first = DMAX;
    cel.end.second = DMAX;
    cel.polygon = -1;
    abb.insert(cel);
    curr.end = DMIN;
    for(auto it = events.begin(); it != events.end(); it++) {
        curr.beg = curr.end;
        curr.end = it->first;
        s.push_back(make_slab(curr, abb));
        for (int i = 0; i < (it->second).size(); i++) {
            if (!(it->second)[i].insert)
                update_abb(abb, (it->second)[i]);
        }
        for (int i = 0; i < (it->second).size(); i++) {
            if ((it->second)[i].insert)
                update_abb(abb, (it->second)[i]);
        }
    }
    curr.beg = curr.end;
    curr.end = DMAX;
    s.push_back(make_slab(curr, abb));
}

int bs(const vector<slab>& s, const pair<double, double> p) {
    int beg = 0, end = s.size() - 1, mid1, mid2;
    
    while (beg < end) {
        mid1 = (beg + end)/2;
        if (s[mid1].beg > p.first) {
            end = mid1 - 1;
        }
        else if (s[mid1].end <= p.first) {
            beg = mid1 + 1;
        }
        else {
            beg = end = mid1;
        }
    }
    mid1 = beg;
    
    beg = 0; end = s[mid1].lines.size() - 1;
    while (beg < end) {
        mid2 = (beg + end)/2;
        if (esquerda(s[mid1].lines[mid2].beg.first, s[mid1].lines[mid2].beg.second, s[mid1].lines[mid2].end.first, s[mid1].lines[mid2].end.second, p.first, p.second)) {
            beg = mid2 + 1;
        }
        else {
            end = mid2;
        }
    }
    mid2 = beg;
    
    return s[mid1].lines[mid2].polygon;
}

void print_slabs(const vector<slab>& s) {
    for (int i = 0; i < s.size(); i++) {
        cout << "beg = " << s[i].beg << endl;
        cout << "end = " << s[i].end << endl;
        cout << "lines:" << endl;
        for (int j = 0; j < s[i].lines.size(); j++) {
            cout << "(" << s[i].lines[j].beg.first << ", " << s[i].lines[j].beg.second << "), (" << s[i].lines[j].end.first << ", " << s[i].lines[j].end.second << "), " << s[i].lines[j].polygon << endl;
        }
        cout << endl;
    }
}

int main() {
	int N, sz, ign;
	cin >> N >> ign;
	vector<vector<pair<double, double> > > polygons(N);
	map<double, vector<evt> > events;
	for (int i = 0; i < N; i++) {
	    cin >> sz >> ign;
	    polygons[i].resize(sz);
	    for (int j = 0; j < sz; j++) {
	        cin >> polygons[i][j].first >> polygons[i][j].second;
	    }
	}
	
	make_events(polygons, events);
	
	//print_events(events);
	
	vector<slab> s;
	make_slabs(s, events);
	
	//print_slabs(s);
	
	int numP;
	cin >> numP >> ign;
	vector<pair<double, double> > points(numP);
	for (int i = 0; i < numP; i++) {
	    cin >> points[i].first >> points[i].second;
	}
	
	for (int i = 0; i < numP; i++) {
	    cout << bs(s, points[i]) << endl;
	}
	
	return 0;
}