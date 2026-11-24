import random


def count_kmers(L, k):
    """길이 L인 서열에 들어 있는 k-mer(겹침 허용)의 개수를 돌려준다.

    한 칸씩 밀면서 자르므로 시작 위치는 0 ~ L-k, 모두 L-k+1 개이다.
    k > L 이면 자를 수 있는 창이 하나도 없으므로 0 을 돌려준다.
    (공식 L-k+1 을 그대로 쓰면 음수가 나오는데, 개수가 음수일 수는 없다.)
    """
    if L < 0:
        raise ValueError("L 은 0 이상이어야 한다")
    if k <= 0:
        raise ValueError("k 는 1 이상이어야 한다")
    if k > L:
        return 0
    return L - k + 1


def count_kmers_direct(L, k):
    """공식 없이 실제 서열을 만들어 k-mer 를 잘라 보고 그 개수를 센다."""
    seq = "".join(random.choice("ACGT") for _ in range(L))
    kmers = []
    for i in range(len(seq) - k + 1):  # k > L 이면 range 가 비어 0 개가 된다
        kmers.append(seq[i:i + k])
    for km in kmers:  # 자른 조각의 길이가 모두 k 인지 확인
        assert len(km) == k
    return len(kmers)


if __name__ == "__main__":
    # 여러 (L, k) 조합: 일반적인 경우, k == L, k == 1, k > L, L == 0
    cases = [(10, 5), (10, 1), (10, 10), (10, 11), (5, 20),
             (100, 21), (1, 1), (0, 3), (1000, 31), (7, 3)]
    print("L\tk\t직접\t함수\t일치")
    for L, k in cases:
        d = count_kmers_direct(L, k)
        f = count_kmers(L, k)
        assert d == f, (L, k, d, f)
        print(f"{L}\t{k}\t{d}\t{f}\t{d == f}")

    # 무작위 조합으로 한 번 더 확인
    for _ in range(1000):
        L = random.randint(0, 200)
        k = random.randint(1, 250)
        assert count_kmers_direct(L, k) == count_kmers(L, k), (L, k)
    print("무작위 1000 개 조합 모두 일치")

    # 잘못된 k 는 오류로 처리
    try:
        count_kmers(10, 0)
    except ValueError as e:
        print("k=0:", e)
