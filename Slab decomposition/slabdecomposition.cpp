#include <bits/stdc++.h>
using namespace std;

double DMIN = -100;
double DMAX = 100;

void make_slabs(vector<pair<double, double> >& slabs, set<double>& xcoords) {
    double lhs, rhs = DMIN;
    for (auto it = xcoords.begin(); it != xcoords.end(); it++) {
        lhs = rhs;
        rhs = *it;
        slabs.push_back({lhs, rhs});
    }
    slabs.push_back({rhs, DMAX});
}

double calcY(pair<double, double> begLine, pair<double, double> endLine, double X) {
    double Y = (X - begLine.first) * (endLine.second - begLine.second);
    Y /= (endLine.first - begLine.first);
    Y += begLine.second;
    return Y;
}

int bsRec(vector<pair<double, double> >& slabs, pair<double, double> p, int beg, int end) {
    int mid = (beg + end)/2;
    if (slabs[mid].first <= p.first && slabs[mid].second >= p.first) {
        return mid;
    }
    else if (slabs[mid].first > p.first) {
        return bsRec(slabs, p, beg, mid - 1);
    }
    return bsRec(slabs, p, mid + 1, end);
}

int bs(vector<pair<double, double> >& slabs, pair<double, double> p) {
    return bsRec(slabs, p, 0, slabs.size());
}
void add_line(vector<vector<tuple<double, double, int> > >& lines, vector<pair<double, double> >& slabs, pair<double, double> beg, pair<double, double> end, int pNum) {
    int aux;
    if (beg.first < end.first) aux = pNum;
    else {
        aux = -1;
        pair<double, double> auxp;
        auxp.first = beg.first; auxp.second = beg.second;
        beg.first = end.first; beg.second = end.second;
        end.first = auxp.first; end.second = auxp.second;
    }
    
    for (int i = bs(slabs, beg); i < bs(slabs, end); i++) {
        lines[i].push_back({calcY(beg, end, slabs[i].first), calcY(beg, end, slabs[i].second), aux});
    }
}

void make_lines(vector<vector<tuple<double, double, int> > >& lines, vector<pair<double, double> >& slabs, vector<vector<pair<double, double> > >& polygons) {
    for (int i = 0; i < polygons.size(); i++) {
        for (int j = 0; j < polygons[i].size(); j++) {
            add_line(lines, slabs, polygons[i][j], polygons[i][(j + 1) % polygons[i].size()], i);
        }
    }
    for (int i = 0; i < slabs.size(); i++) {
        lines[i].push_back({DMAX, DMAX, -1});
        sort(lines[i].begin(), lines[i].end());
        lines[i].erase(unique(lines[i].begin(), lines[i].end()), lines[i].end());
    }
}

bool esquerda(double X1, double Y1, double X2, double Y2, double X3, double Y3) {
    return ((X2 - X1) * (Y3 - Y1) - (X3 - X1) * (Y2 - Y1) >= 0);
}

int bsPointLines(vector<tuple<double, double, int> >& lines, pair<double, double> slab, pair<double, double> p, int beg, int end) {
    int mid = (beg + 1 + end)/2;
    if (mid == 0) return mid;
    if (esquerda(slab.first, get<0>(lines[mid]), slab.second, get<1>(lines[mid]), p.first, p.second)) {
        return bsPointLines(lines, slab, p, mid, end);
    }
    if (!esquerda(slab.first, get<0>(lines[mid - 1]), slab.second, get<1>(lines[mid - 1]), p.first, p.second)) {
        return bsPointLines(lines, slab, p, beg, mid - 1);
    }
    return mid;
}

int main() {
	
	/*
	Input: first line: N (number of polygons)
	for each polygon:  first line: P (number of points)
	                   next P lines: X Y (coordinates for each point)
	                   M (number of teste points)
	next M lines:      X Y (coordinates for each point)
	*/
	
	int N, sz;
	cin >> N;
	vector<vector<pair<double, double> > > polygons(N);
	set<double> xcoords;
	for (int i = 0; i < N; i++) {
	    cin >> sz;
	    polygons[i].resize(sz);
	    for (int j = 0; j < sz; j++) {
	        cin >> polygons[i][j].first >> polygons[i][j].second;
	        xcoords.insert(polygons[i][j].first);
	    }
	}
	
	vector<pair<double, double> > slabs;
	make_slabs(slabs, xcoords);
	
	vector<vector<tuple<double, double, int> > > lines(slabs.size());
	make_lines(lines, slabs, polygons);
	
	int numP;
	int s, l;
	cin >> numP;
	vector<pair<double, double> > points(numP);
	for (int i = 0; i < numP; i++) {
	    cin >> points[i].first >> points[i].second;
	}
	
	for (int i = 0; i < numP; i++) {
	    s = bs(slabs, points[i]);
	    l = bsPointLines(lines[s], slabs[s], points[i], 0, lines[s].size() - 1);
	    cout << get<2>(lines[s][l]) << endl;
	}
	return 0;
}
