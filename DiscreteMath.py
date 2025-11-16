SIZE = 5

# 관계 행렬 입력
# 5 * 5 크기 정방행렬 -> 행단위 입력
# 입력 데이터 : list (2차원 배열)로 저장
# 집합 A = {1, 2, 3, 4, 5}의 관계 행렬을 입력
def input_relation_matrix():
    mat = []
    for _ in range(SIZE):
        input_ = list(map(int, input().split()))
        mat.append(input_)

    return mat

# 반사 관계인지
# 관계행렬의 모든 대각 원소가 1인지 확인
def is_reflection(relationMat):
    for i in range(SIZE):
        if relationMat[i][i] != 1:
            return False
    return True

# 대칭 관계인지
# 행렬이 자신을 전치시킨 것과 같아야 함
def is_summetry(relationMat):
    transpose = []

    for i in range(SIZE):
        temp = []
        for j in range(SIZE):
            temp.append(relationMat[j][i])
        transpose.append(temp)

    for i in range(SIZE):
        for j in range(SIZE):
            if relationMat[i][j] != transpose[i][j]:
                return False

    return True

# 추이 관계인지
def is_transition(relationMat):
    for i in range(SIZE):
        for j in range(SIZE):
            if relationMat[i][j] == 1:
                for k in range(SIZE):
                    if relationMat[j][k] == 1 and relationMat[i][k] == 0:
                        return False
    return True


# 동치 관계인지
def is_equivalent(relationMat):
    if is_reflection(relationMat) and is_summetry(relationMat) and is_transition(relationMat):
        return True
    return False

# 동치관계라면 동치류 출력
def print_equivalence_class(relationMat):
    if not is_equivalent(relationMat):
        return []

    visited = [False for _ in range(SIZE)]
    classes = []

    for i in range(SIZE):
        if visited[i]:
            continue

        eq_class = []
        for j in range(SIZE):
            if relationMat[i][j] == relationMat[j][i] == 1:
                eq_class.append(j)

        for j in range(len(eq_class)):
            visited[eq_class[j]] = True
            eq_class[j] += 1

        classes.append(eq_class)

    return classes

def make_reflection_alveoli(relationMat):
    mat = [row[:] for row in relationMat]

    for i in range(SIZE):
        mat[i][i] = 1

    return mat

def make_summetry_alveoli(relationMat):
    mat = [row[:] for row in relationMat]

    for i in range(SIZE):
        for j in range(SIZE):
            if mat[i][j] == 1:
                mat[j][i] = 1

    return mat

def make_transition_alveoli(relationMat):
    mat = [row[:] for row in relationMat]
    is_not_stable = True

    while (is_not_stable):
        is_not_stable = False

        for i in range(SIZE):
            for j in range(SIZE):
                if mat[i][j] == 1:
                    for k in range(SIZE):
                        if mat[j][k] == 1 and mat[i][k] == 0:
                            mat[i][k] = 1
                            print(f"({i}, {k})를 추가")
                            is_not_stable = True
    
    return mat

def make_transition_warshall(relationMat):
    mat = [row[:] for row in relationMat]
    for k in range(SIZE):
        for i in range(SIZE):
            for j in range(SIZE):
                if mat[i][k] and mat[k][j]:
                    mat[i][j] = 1

    return mat

def print_mat(mat):
    for row in mat:
        for col in row:
            print(col, end=" ")
        print()

# 각 관계를 성립하지 못 할 때, 폐포 만들기
# 변환 전 , 변환 후 출력
# 각 폐포로 변환한 후 동치 관계 다시 판별하고, 동치류 출력
def make_alveoli(relationMat):
    copy_relationMat = [row[:] for row in relationMat]

    if not is_reflection(relationMat):
        print("반사 폐포 발생: ")
        mat = make_reflection_alveoli(copy_relationMat)
        print("==========변경 전================")
        print_mat(relationMat)
        print("==========변경 후================")
        print_mat(mat)
        copy_relationMat = [[ mat[i][j] | copy_relationMat[i][j] for j in range(SIZE)] for i in range(SIZE)]

    if not is_summetry(relationMat):
        print("대칭 폐포 발생: ")
        mat = make_summetry_alveoli(copy_relationMat)
        print("==========변경 전================")
        print_mat(relationMat)
        print("==========변경 후================")
        print_mat(mat)
        copy_relationMat = [[ mat[i][j] | copy_relationMat[i][j] for j in range(SIZE)] for i in range(SIZE)]

    if not is_transition(copy_relationMat):
        print("추이 폐포 발생(반사, 대칭 이미 만족한 경우): ")

        mat = make_transition_alveoli(copy_relationMat)
        warshallMat = make_transition_warshall(copy_relationMat)
        print("==========변경 전================")
        print_mat(copy_relationMat)
        print("==========변경 후================")
        print_mat(mat)
        copy_relationMat = [[ mat[i][j] | copy_relationMat[i][j] for j in range(SIZE)] for i in range(SIZE)]

    return copy_relationMat


if __name__ == "__main__":
    set_ = [1, 2, 3, 4, 5]

    print ("관계행렬을 입력하시오. (행 단위로, 각 원소는 한 칸의 공백):")
    relationMat = input_relation_matrix()

    print("반사 관계를 만족하나요? : " + str(is_reflection(relationMat)))
    print("대칭 관계를 만족하나요? : " + str(is_summetry(relationMat)))
    print("추이 관계를 만족하나요? : " + str(is_transition(relationMat)))
    print("동치 관계를 만족하나요? : " + str(is_equivalent(relationMat)))

    print()

    print("동치 관계를 만족했을 때, 동치류는? (만족하지 않으면 [] 출력) : ", end="")
    print(print_equivalence_class(relationMat))

    print("\n")

    print("폐포 구현: ")
    equivalent_alveoli = make_alveoli(relationMat)
    print("동치 관계를 만족하나요? : " + str(is_equivalent(equivalent_alveoli)))

    print("동치 관계를 만족했을 때, 동치류는? (만족하지 않으면 [] 출력) : ", end="")
    print(print_equivalence_class(equivalent_alveoli))

