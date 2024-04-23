
mkdir -p study/code
mkdir -p study/rawdata
for sub in 01 02; do
  mkdir -p study/derivatives/sub-${sub}/dummy
  d=study/rawdata/sub-${sub}/ses-01/anat
  mkdir -p ${d}
  for i in 400 800; do
    touch ${d}/sub-${sub}_ses-01_inv-${i}_IRT1.nii.gz
    touch ${d}/sub-${sub}_ses-01_inv-${i}_IRT1.json
  done
done