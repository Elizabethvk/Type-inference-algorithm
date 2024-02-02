// fn f(x: i32) -> i32 {
//     return x * 2;
// }

fn f(x) { 
    return x[2];
}

fn f(x) { 
    return x*2;
}

fn f(b) {
    var x;
    if(b)
    {
        x = "Hello";
    } else {
        x = 3;
    }
    return x;
}

fn f(b) {
    var x;
    if(b)
    {
        x = "Hello";
    }
    return x;
}

fn f(n)
{
    if(n == 0)
    {
        return 1;
    } else if(n == 1)
    {
        return 1;
    }
    return f(n-1) + f(n-2);
}