# Tri2NURBS
* Input: triangular mesh
* Output: a conforming quad layout, followed by NURBS interpolation.

## Frist step: compute eigen functions
```python
eigens(input, 'EigenFunctions', num)
```

## Second step: Morse Smale Quadrangulation
```python
morseSmaleQuadrangulation("EigenFunctions.vtu", "./Quadrangulation", num, start)
```

## Third step: singularities and separatrices 
```python
pt_list, idx_patches = conformal_patch_gen(f'./Quadrangulation/EigenFunction{id}.obj')
```

## Fourth step: NURBS multi-patch surface approximation
```python
degree_us,degree_vs,kv_us,kv_vs,ctrlpts_size_us,ctrlpts_size_vs,ctrlpts,weights=approximate_mp_nurbs_surf(pt_list, idx_patches,max_deg,ctrlpts_size)
```


    
