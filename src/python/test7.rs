fn f(n) {
    if n == 0 {
        return 1;
    } else {
        return n * g(n - 1);
    }
}

fn g(m) {
    if m == 1 {
        return 1;
    } else {
        return m * f(m - 1);
    }
}