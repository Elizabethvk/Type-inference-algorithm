fn f(n)
{
    if(n == 0)
    {
        return 1
    } else if(n == 1)
    {
        return 1
    }
    return f(n-1) + f(n-2)
}